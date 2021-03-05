import csv
import requests
import yaml

from pathlib import Path
from string import ascii_letters

from oc_web_scraper import errors as _CUSTOM_ERRORS
from oc_web_scraper.library import Library
from oc_web_scraper.category import Category


class Saver:
    """Saver class manages local saving process.
    It exploits Library object created during scrapping to
    create a csv file for each category and save the book
    cover image for each book.

    Attributes:
        config (dict): Parsed content of config.yml file.
    """

    def __init__(self):
        """Constructor for Saver class."""

        config = None

        self.parse_config()

    def parse_config(self):

        package_dir = Path(__file__).parent
        config_path = package_dir.joinpath("config.yml").resolve()

        with open(str(config_path)) as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

        self.save_path_exists()

    def save_path_exists(self):
        """Verifies if path input in config.yml exists

        Raises:
            _CUSTOM_ERRORS.SavePathDoesNotExists: If save path input in
            config.yml file does not exists.

        Returns:
            bool: Path exists.
        """
        path_object = Path(self.config["save_path"])

        if not path_object.exists():
            raise _CUSTOM_ERRORS.SavePathDoesNotExists(self.config["save_path"])

        return True

    def save_library(self, library: Library):
        """Drives the saving process by iterating through Library categories.

        Args:
            library (Library): Library object created by Handler.
        """

        for category in library.categories:
            category_object = library.categories[category]
            category_name = category_object.name

            category_path = self.get_category_path(category_name=category_name)
            self.create_category_dir(category_path)

            self.save_category(
                category_books=category_object.books,
                category_name=category_name,
                category_path=category_path,
            )

    def save_category(
        self, category_books: dict, category_name: str, category_path: Path
    ):
        """Particular saving process by category. Iterates through Books to
        store their value for the [category_name].csv file and scrap/save
        their cover image.

        Args:
            category (dict): Books attribute of Category.
            category_name (str): Name of the category.
            category_path (Path): Local save path for this category.
        """

        csv_rows = []

        for book in category_books:
            book_object = category_books[book]
            csv_rows.append(
                {
                    "URL": book_object.url,
                    "UPC": book_object.upc,
                    "Title": book_object.title,
                    "Price Including Tax": book_object.price_including_tax,
                    "Price Excluding Tax": book_object.price_excluding_tax,
                    "Number Available": book_object.number_available,
                    "Product Description": book_object.product_description,
                    "Category": book_object.category,
                    "Review Rating": book_object.review_rating,
                    "Image URL": book_object.image_url,
                }
            )
            self.save_image(
                book_title=book_object.title,
                image_url=book_object.image_url,
                category_path=category_path,
            )

        self.save_csv(
            category_name=category_name, csv_rows=csv_rows, category_path=category_path
        )

    def slugify(self, raw_string: str):
        """Transforms raw name to slug to avoid any file/dir naming problems.

        Args:
            raw_string (str): Raw name to be slugified

        Returns:
            str: Slugified name
        """

        slug = ""

        for char in raw_string:
            if char in ascii_letters:
                slug += char.lower()
            elif char == " ":
                slug += "_"

        return slug.strip("_")

    def backup_csv_file(self, csv_file: Path):
        """Create a .backup for csv file if it already exists.

        Args:
            csv_file (Path): csv file absolute file
        """

        backup_file = Path(csv_file.parent / (csv_file.name + ".backup"))

        if backup_file.exists():
            backup_file.unlink()

        csv_file.rename(backup_file)

    def get_category_path(self, category_name: str):
        """Returns adequate path for category dir by
        turning its raw name to a slug.

        Args:
            category_name (str): Raw category name.

        Returns:
            str: Path to save category scrapped content.
        """

        category_slug = self.slugify(category_name)

        category_path = Path(self.config["save_path"]).joinpath(category_slug)

        return category_path

    def create_category_dir(self, path: Path):
        """Creates category directory and a child 'images' directory
        to save scrapped content.

        Args:
            path (Path): Absolute path for category directory.
        """

        image_path = path.joinpath("images")

        Path(path).mkdir(exist_ok=True)
        Path(image_path).mkdir(exist_ok=True)

    def save_image(self, book_title: str, image_url: str, category_path: Path):
        """Scrap book cover image and saves it locally.

        Args:
            book_title (str): Book title for local file name.
            image_url (str): Book cover image URL.
            category_path (Path): Category absolute local path for saving.

        Raises:
            _CUSTOM_ERRORS.FailedToSaveImage: If GET request returns an error.
        """

        img_response = requests.get(image_url, stream=True, allow_redirects=True)

        if img_response.status_code != 200:
            raise _CUSTOM_ERRORS.FailedToSaveImage(title=book_title, url=image_url)

        image_dir = category_path.joinpath("images")
        book_slug = self.slugify(book_title)
        image_file = image_dir.joinpath(book_slug + ".jpg")

        with open(image_file, "wb") as out_file:
            out_file.write(img_response.content)

    def save_csv(self, category_name: str, csv_rows: dict, category_path: Path):
        """Manages saving a category stored values to a csv file.

        Args:
            category_name (str): Raw category name.
            csv_rows (list): List of dicts representing per books values.
            category_path (Path): Category absolute local path for saving.
        """

        csv_fieldnames = [
            "URL",
            "UPC",
            "Title",
            "Price Including Tax",
            "Price Excluding Tax",
            "Number Available",
            "Product Description",
            "Category",
            "Review Rating",
            "Image URL",
        ]

        category_slug = self.slugify(category_name)
        csv_file_path = category_path.joinpath("{slug}.csv".format(slug=category_slug))

        if csv_file_path.exists():
            self.backup_csv_file(csv_file=csv_file_path)

        with open(csv_file_path, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames)
            writer.writeheader()
            for data in csv_rows:
                writer.writerow(data)

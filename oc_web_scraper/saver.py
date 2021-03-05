import csv

from pathlib import Path, PurePath
from string import ascii_letters, punctuation

from oc_web_scraper import errors as _CUSTOM_ERRORS
from oc_web_scraper.library import Library
from oc_web_scraper.category import Category
from oc_web_scraper.book import Book

_SAVE_PATH = "/tmp/"

# Format:
# data/NomDelaCategory/NomDelaCategory.csv
# data/NomDelaCategory/Image/TitreDulivre.jpg


def slugify(raw_string: str):
    slug = ""

    raw_string = raw_string.strip()

    for char in raw_string:
        if char in ascii_letters:
            slug += char.lower()
        elif char == " ":
            slug += "_"

    return slug


def save_path_exists(save_path: str):
    path_object = Path(save_path)

    if not path_object.exists():
        raise _CUSTOM_ERRORS.SavePathDoesNotExists(save_path)

    return True


def backup_csv_file(csv_file: Path):
    pass


def get_category_path(save_path: str, category_name: str):
    category_slug = slugify(category_name)

    category_path = Path(save_path).joinpath(category_slug)

    return category_path


def create_category_dir(path: Path):

    image_path = path.joinpath("images")

    Path(path).mkdir(exist_ok=True)
    Path(image_path).mkdir(exist_ok=True)


def save_csv(category_name: str, csv_rows: dict, category_path: Path):
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

    category_slug = slugify(category_name)
    csv_file_path = category_path.joinpath("{slug}.csv".format(slug=category_slug))

    if csv_file_path.exists():
        backup_csv_file(csv_file=csv_file_path)

    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames)
        writer.writeheader()
        for data in csv_rows:
            writer.writerow(data)


def save_category(category: Category, category_name: str, category_path: Path):

    csv_rows = []

    for book in category.books:
        book_object = category.books[book]
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

    save_csv(
        category_name=category_name, csv_rows=csv_rows, category_path=category_path
    )


def save_library(library: Library, save_path: str):

    for category in library.categories:
        category_object = library.categories[category]
        category_name = category_object.name

        category_path = get_category_path(
            save_path=save_path, category_name=category_name
        )
        create_category_dir(category_path)

        save_category(
            category=category_object,
            category_name=category_name,
            category_path=category_path,
        )

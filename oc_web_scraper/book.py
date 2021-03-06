import re
import requests

from bs4 import BeautifulSoup, element

from oc_web_scraper import errors as _CUSTOM_ERRORS
from oc_web_scraper.logger import Logger


class Book:
    """Book class manages book page scraping and
    stores its unique product information.

    Attributes:
        logger (Logger): Main app logger object. Passed in instantiation arguments.
        image_relative_path (str): Relative path hard-coded in image URLs.
        image_absolute_path (str): Absolute equivalent of the relative path.
        title (str): Book title. Passed in instantiation arguments.
        url (str): Book page URL. Passed in instantiation arguments.
        category (str): Book category. Passed in instantiation arguments.
        product_description (str): Product description, set during infos scraping.
        upc (str): UPC, set during infos scraping.
        price_including_tax (str): Price including tax, set during infos scraping.
        price_excluding_tax (str): Price excluding tax, set during infos scraping.
        number_available (str): Number of books available, set during infos scraping.
        review_rating (str): Review rating, set during infos scraping.
        image_url (str): Book cover image URL, set during infos scraping."""

    def __init__(self, title: str, url: str, category: str, logger: Logger):
        """Constructor for Book class.

        Args:
            title (str): Book title.
            url (str): Book page URL.
            category (str): Category of the book.
            logger (Logger): Main app logger object.
        """

        self.logger = logger

        # Image URL relative part and its absolute equivalent
        # are hard coded to ease eventual adaptation for
        # future website structure modifications.
        self.image_relative_path = "../../"
        self.image_absolute_path = "https://books.toscrape.com/"

        self.title = title
        self.url = url
        self.category = category

        self.logger.write(
            log_level="info",
            message="Created book titled {title}.".format(title=self.title),
        )

        self.product_description = None
        self.upc = None
        self.price_including_tax = None
        self.price_excluding_tax = None
        self.number_available = None
        self.review_rating = None
        self.image_url = None

        self.scrap_book()

    def __str__(self):
        stdout_content = " - Title: {title}\n".format(title=self.title)
        stdout_content += "  - URL: {url}\n\n".format(url=self.url)
        stdout_content += "  - Description: {description}\n\n".format(
            description=self.product_description
        )
        stdout_content += "  - UPC: {upc}\n".format(upc=self.upc)
        stdout_content += "  - Price Including Tax: {price}\n".format(
            price=self.price_including_tax
        )
        stdout_content += "  - Price Excluding Tax: {price}\n".format(
            price=self.price_excluding_tax
        )
        stdout_content += "  - Number Available: {number}\n".format(
            number=self.number_available
        )
        stdout_content += "  - Review rating: {rating}\n".format(
            rating=self.review_rating
        )
        stdout_content += "  - Image URL: {url}\n".format(url=self.image_url)

        return stdout_content

    def scrap_book(self):
        """Scraping process for book pages.
        Relevant infos are picked using bs4 and stored in class
        attributes.
        """

        soup = self.create_soup()

        self.set_image_url(soup=soup)
        self.set_rating(soup=soup)
        self.set_product_description(soup=soup)
        self.set_product_info(soup=soup)

    def create_soup(self):
        """Create a BeautifulSoup object from raw request response.

        Raises:
            _CUSTOM_ERRORS.CouldNotGetBookPage: If response code is
            different from 200.

        Returns:
            BeautifulSoup: Object to work with during further scraping.
        """

        raw_response = requests.get(self.url)

        if raw_response.status_code != 200:
            self.logger.write(
                log_level="error",
                message="Bad status code received from request to website.",
            )
            raise _CUSTOM_ERRORS.CouldNotGetBookPage(url=self.url)

        self.logger.write(
            log_level="debug",
            message="Received response for book page with status code 200.",
        )

        soup = BeautifulSoup(raw_response.content, "html.parser")

        return soup

    def set_image_url(self, soup: BeautifulSoup):
        """Find the book cover image in the page and sets the image_url
        attribute to its absolute path.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the book page.

        Raises:
            _CUSTOM_ERRORS.NoImageFound: If book cover is not found in page.
        """

        raw_image = soup.find("img", attrs={"alt": self.title})

        if raw_image is None:
            self.logger.write(
                log_level="error",
                message="No image found on book page.",
            )
            raise _CUSTOM_ERRORS.NoImageFound(self.title, url=self.url)

        image_relative_url = raw_image["src"]
        image_absolute_url = image_relative_url.replace(
            self.image_relative_path, self.image_absolute_path
        )

        self.image_url = image_absolute_url

    def set_rating(self, soup: BeautifulSoup):
        """Finds the review rating element in the page then calls
        convert_rating to convert it to int and set object attribute.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the book page.

        Raises:
            _CUSTOM_ERRORS.NoRatingFound: If book rating is not found in page.
        """

        raw_rating = soup.select('p[class*="star-rating"]')

        if len(raw_rating) == 0:
            self.logger.write(
                log_level="error",
                message="No rating found on book page.",
            )
            raise _CUSTOM_ERRORS.NoRatingFound(self.title, url=self.url)

        self.convert_rating(raw_rating=raw_rating[0])

    def convert_rating(self, raw_rating: element.Tag):
        """Converts string literal rating values to int value
        from the raw rating DOM element class attributes.

        Args:
            raw_rating (element.Tag): Raw DOM element scrapped beforehand.

        Raises:
            _CUSTOM_ERRORS.FailedToGetRating: If class attributes literal does not
            match any rating from 0 to 5.
        """

        class_attributes = raw_rating["class"]

        if "Zero" in class_attributes:
            self.review_rating = 0
        elif "One" in class_attributes:
            self.review_rating = 1
        elif "Two" in class_attributes:
            self.review_rating = 2
        elif "Three" in class_attributes:
            self.review_rating = 3
        elif "Four" in class_attributes:
            self.review_rating = 4
        elif "Five" in class_attributes:
            self.review_rating = 5
        else:
            raise _CUSTOM_ERRORS.FailedToGetRating(class_attributes)

    def set_product_description(self, soup: BeautifulSoup):
        """Finds the product description, if present, in book page.
        Then sets object attribute.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the book page.

        Raises:
            _CUSTOM_ERRORS.NoProductDescriptionFound: If book description is
            found in page but proper text is not.
        """

        raw_product_description_title = soup.find(
            "div", attrs={"id": "product_description"}
        )

        # Allow empty description, which occurs.
        if raw_product_description_title is not None:
            raw_product_description = raw_product_description_title.find_next("p")
            if raw_product_description is None:
                self.logger.write(
                    log_level="error",
                    message="No product description found on book page.",
                )
                raise _CUSTOM_ERRORS.NoProductDescriptionFound(self.title, url=self.url)

            self.product_description = raw_product_description.get_text().strip()

    def set_product_info(self, soup: BeautifulSoup):
        """Finds the product info container element in the page then calls
        parse_product_info to parse it and set object attributes.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the book page.

        Raises:
            _CUSTOM_ERRORS.NoProductInformationFound: If book information
            container is not found in page.
        """

        raw_product_information = soup.find(
            "table", attrs={"class": "table table-striped"}
        )

        if raw_product_information is None:
            self.logger.write(
                log_level="error",
                message="No product information found on book page.",
            )
            raise _CUSTOM_ERRORS.NoProductInformationFound(self.title, url=self.url)

        self.parse_product_info(raw_product_information)

    def parse_product_info(self, raw_info: element.Tag):
        """Parses informations displayed within the information
        container and set class attributes values.

        Args:
            raw_info (element.Tag): Raw DOM element scrapped beforehand.

        Raises:
            _CUSTOM_ERRORS.BookInfoParsingFailed: If at least one of the
            searched informations is missing.
        """

        info_lines = raw_info.find_all("tr")

        for line in info_lines:
            line_text = line.get_text()

            if "UPC" in line_text:
                self.set_upc(raw_line=line)
            elif "Price (incl. tax)" in line_text:
                self.set_price_including_tax(raw_line=line)
            elif "Price (excl. tax)" in line_text:
                self.set_price_excluding_tax(raw_line=line)
            elif "Availability" in line_text:
                self.set_number_available(raw_line=line)

        # After parsing, verify if all infos were found.
        mandatory_attr_not_set = [
            self.upc is None,
            self.price_including_tax is None,
            self.price_excluding_tax is None,
            self.number_available is None,
        ]

        if any(mandatory_attr_not_set):
            self.logger.write(
                log_level="error",
                message="Book informations parsing failed.",
            )
            raise _CUSTOM_ERRORS.BookInfoParsingFailed(title=self.title, url=self.url)

    def set_upc(self, raw_line: element.Tag):
        """Sets upc class attribute from raw DOM element.

        Args:
            raw_line (element.Tag): Raw DOM element.

        Raises:
            _CUSTOM_ERRORS.CouldNotParseInfo: If the info cannot be found.
            Missing info will be mentionned in error message.
        """

        value = raw_line.find("td")

        if value is None:
            self.logger.write(
                log_level="error",
                message="Could not parse UPC on book page.",
            )
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="UPC", url=self.url
            )

        self.upc = value.get_text().strip()

    def set_price_including_tax(self, raw_line: element.Tag):
        """Sets price_including_tax class attribute from raw DOM element.

        Args:
            raw_line (element.Tag): Raw DOM element.

        Raises:
            _CUSTOM_ERRORS.CouldNotParseInfo: If the info cannot be found.
            Missing info will be mentionned in error message.
        """

        value = raw_line.find("td")

        if value is None:
            self.logger.write(
                log_level="error",
                message="Could not parse Price incl. tax on book page.",
            )
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Price including Tax", url=self.url
            )

        self.price_including_tax = value.get_text().strip()

    def set_price_excluding_tax(self, raw_line: element.Tag):
        """Sets price_excluding_tax class attribute from raw DOM element.

        Args:
            raw_line (element.Tag): Raw DOM element.

        Raises:
            _CUSTOM_ERRORS.CouldNotParseInfo: If the info cannot be found.
            Missing info will be mentionned in error message.
        """

        value = raw_line.find("td")

        if value is None:
            self.logger.write(
                log_level="error",
                message="Could not parse Price excl. tax on book page.",
            )
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Price excluding Tax", url=self.url
            )

        self.price_excluding_tax = value.get_text().strip()

    def set_number_available(self, raw_line: element.Tag):
        """Sets number_available class attribute from raw DOM element.

        Args:
            raw_line (element.Tag): Raw DOM element.

        Raises:
            _CUSTOM_ERRORS.CouldNotParseInfo: If the info cannot be found.
            Missing info will be mentionned in error message.
        """

        value = raw_line.find("td")

        if value is None:
            self.logger.write(
                log_level="error",
                message="Could not parse number of books available on book page.",
            )
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Number available", url=self.url
            )

        number = re.findall("([0-9]+) available", value.get_text())

        if len(number) == 0:
            self.logger.write(
                log_level="error",
                message="Could not parse number of books available on book page.",
            )
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Number available", url=self.url
            )

        self.number_available = int(number[0])
import requests
import re

from bs4 import BeautifulSoup
from bs4 import element

from oc_web_scraper import errors as _CUSTOM_ERRORS


class Book:
    def __init__(self, title: str, url: str, category: str):

        self.image_relative_path = "../../"
        self.image_absolute_path = "https://books.toscrape.com"

        self.title = title
        self.url = url
        self.category = category

        self.product_description = None
        self.upc = None
        self.price_including_tax = None
        self.price_excluding_tax = None
        self.number_available = None
        self.product_description = None
        self.review_rating = None
        self.image_url = None

        self.scrap_book()
        print(self)

    def __str__(self):

        print_content = " - Title: {title}\n".format(title=self.title)
        print_content += "  - URL: {url}\n\n".format(url=self.url)
        print_content += "  - Description: {description}\n\n".format(
            description=self.product_description
        )
        print_content += "  - UPC: {upc}\n".format(upc=self.upc)
        print_content += "  - Price Including Tax: {price}\n".format(
            price=self.price_including_tax
        )
        print_content += "  - Price Excluding Tax: {price}\n".format(
            price=self.price_excluding_tax
        )
        print_content += "  - Number Available: {number}\n".format(
            number=self.number_available
        )
        print_content += "  - Review rating: {rating}\n".format(
            rating=self.review_rating
        )
        print_content += "  - Image URL: {url}\n".format(url=self.image_url)

        return print_content

    def scrap_book(self):
        raw_response = requests.get(self.url)
        soup = BeautifulSoup(raw_response.content, "html.parser")

        raw_image = soup.find("img", attrs={"alt": self.title})

        if raw_image is None:
            raise _CUSTOM_ERRORS.NoImageFound(self.title)

        image_relative_url = raw_image["src"]
        image_absolute_url = image_relative_url.replace(
            self.image_relative_path, self.image_absolute_path
        )

        self.image_url = image_absolute_url

        raw_rating = soup.select('p[class*="star-rating"]')

        if len(raw_rating) == 0:
            raise _CUSTOM_ERRORS.NoRatingFound(self.title)

        self.set_rating(raw_rating=raw_rating[0])

        raw_product_description_title = soup.find(
            "div", attrs={"id": "product_description"}
        )

        if raw_product_description_title is None:
            raise _CUSTOM_ERRORS.NoProductDescriptionFound(self.title)

        raw_product_description = raw_product_description_title.find_next("p")

        if raw_product_description is None:
            raise _CUSTOM_ERRORS.NoProductDescriptionFound(self.title)

        self.product_description = raw_product_description.get_text().strip()

        raw_product_information = soup.find(
            "table", attrs={"class": "table table-striped"}
        )

        if raw_product_information is None:
            raise _CUSTOM_ERRORS.NoProductInformationFound(self.title)

        self.parse_product_info(raw_product_information)

    def set_rating(self, raw_rating: str):
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

    def parse_product_info(self, raw_info: element.Tag):
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

        mandatory_attr_not_set = [
            self.upc is None,
            self.price_including_tax is None,
            self.price_excluding_tax is None,
            self.number_available is None,
        ]

        if any(mandatory_attr_not_set):
            raise _CUSTOM_ERRORS.BookInfoParsingFailed(title=self.title)

    def set_upc(self, raw_line: element.Tag):
        value = raw_line.find("td")

        if value is None:
            raise _CUSTOM_ERRORS.CouldNotParseInfo(title=self.title, info="UPC")

        self.upc = value.get_text().strip()

    def set_price_including_tax(self, raw_line: element.Tag):
        value = raw_line.find("td")

        if value is None:
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Price including Tax"
            )

        self.price_including_tax = value.get_text().strip()

    def set_price_excluding_tax(self, raw_line: element.Tag):
        value = raw_line.find("td")

        if value is None:
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Price excluding Tax"
            )

        self.price_excluding_tax = value.get_text().strip()

    def set_number_available(self, raw_line: element.Tag):
        value = raw_line.find("td")

        if value is None:
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Number available"
            )

        number = re.findall("([0-9]+) available", value.get_text())

        if len(number) == 0:
            raise _CUSTOM_ERRORS.CouldNotParseInfo(
                title=self.title, info="Number available"
            )

        self.number_available = int(number[0])
import requests
import yaml

from pathlib import Path
from bs4 import BeautifulSoup, element

from oc_web_scraper import errors as _CUSTOM_ERRORS

from oc_web_scraper.saver import Saver
from oc_web_scraper.logger import Logger
from oc_web_scraper.library import Library


class Handler:
    """Handler class drives the entire app process.
    It parses config from config.yaml, instantiate logger
    and saver objects.
    Then, start scraping main page and populates main
    Library object."""

    def __init__(self, website_url: str):
        """Constructor for Handler class.

        Args:
            website_url (str): Website root url.
        """

        self.config = None
        self.parse_config()

        self.logger = Logger(
            enable_logging=self.config["enable_logging"],
            log_to_file=self.config["log_to_file"],
            log_path=self.config["log_path"],
            log_level=self.config["log_level"],
        )
        self.saver = Saver(save_path=self.config["save_path"], logger=self.logger)

        self.website_url = website_url
        self.library = Library(logger=self.logger)

        self.scrap_homepage()

        self.saver.save_library(self.library)

    def parse_config(self):
        """Parses configuration from the config.yaml to a dict."""

        package_dir = Path(__file__).parent
        config_path = package_dir.joinpath("config.yml").resolve()

        with open(str(config_path)) as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    def scrap_homepage(self):
        """Home page scraping process.
        Drives the library's categories increment.
        """

        soup = self.create_soup()

        raw_category_list = self.find_category_list(soup=soup)

        self.instantiate_categories(raw_category_list=raw_category_list)

    def create_soup(self):
        """Create a BeautifulSoup object from raw request response.

        Raises:
            _CUSTOM_ERRORS.CouldNotGetMainPage: If response code is
            different from 200.

        Returns:
            BeautifulSoup: Object to work with during further scraping.
        """

        raw_response = requests.get(self.website_url)

        if raw_response.status_code != 200:
            self.logger.write(
                log_level="error",
                message="Bad status code received from request to website.",
            )
            raise _CUSTOM_ERRORS.CouldNotGetCategoryPage(url=self.website_url)

        self.logger.write(
            log_level="debug",
            message="Received response for main page with status code 200.",
        )

        soup = BeautifulSoup(raw_response.content, "html.parser")

        return soup

    def find_category_list(self, soup: BeautifulSoup):
        """Find the left hand category list on main page
        and returns its contained elements.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the main page.

        Raises:
            _CUSTOM_ERRORS.NoCategoryContainerFound: If the category
            container element is not found in the page.
            _CUSTOM_ERRORS.NoCategoryFound: If no category is found within
            the container.

        Returns:
            element.ResultSet: bs4 resultset of all categories
            in category list.
        """

        category_container = soup.find("div", attrs={"class": "side_categories"})

        if category_container is None:
            self.logger.write(
                log_level="error",
                message="Failed to find the category container in main page.",
            )
            raise _CUSTOM_ERRORS.NoCategoryContainerFound

        raw_category_list = category_container.find_all("li")

        if raw_category_list is None:
            self.logger.write(
                log_level="error",
                message="Failed to find the list of categories in main page.",
            )
            raise _CUSTOM_ERRORS.NoCategoryFound

        return raw_category_list

    def instantiate_categories(self, raw_category_list: element.ResultSet):
        """Parse categories in previously found results and instantiate
        Category objects with library.create_category method.

        Args:
            raw_category_list (element.ResultSet): Results previously scrapped.
        """

        for cat in raw_category_list:
            url = cat.find("a")["href"]

            # Ignore main <li> tag
            if "books_1" in url:
                continue

            name = cat.get_text().strip()

            self.library.create_category(name=name, url=self.website_url + url)

            # Breaking after first cat is scrapped
            # for dev purposes
            break
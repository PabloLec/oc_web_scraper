import requests
import yaml

from pathlib import Path
from bs4 import BeautifulSoup

from oc_web_scraper import errors as _CUSTOM_ERRORS

from oc_web_scraper.saver import Saver
from oc_web_scraper.logger import Logger
from oc_web_scraper.library import Library


class Handler:
    def __init__(self, website_url: str):
        self.config = None
        self.parse_config()

        self.saver = Saver(save_path=self.config["save_path"])
        self.logger = Logger(
            enable_logging=self.config["enable_logging"],
            log_to_file=self.config["log_to_file"],
            log_path=self.config["log_path"],
            log_level=self.config["log_level"],
        )

        self.website_url = website_url
        self.library = Library()

        self.scrap_homepage()

        self.saver.save_library(self.library)

    def parse_config(self):
        package_dir = Path(__file__).parent
        config_path = package_dir.joinpath("config.yml").resolve()

        with open(str(config_path)) as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    def scrap_homepage(self):
        raw_response = requests.get(self.website_url)

        if raw_response.status_code != 200:
            raise _CUSTOM_ERRORS.CouldNotGetMainPage(url=self.website_url)

        soup = BeautifulSoup(raw_response.content, "html.parser")

        category_container = soup.find("div", attrs={"class": "side_categories"})

        if category_container is None:
            raise _CUSTOM_ERRORS.NoCategoryContainerFound

        raw_categories_list = category_container.find_all("li")

        if raw_categories_list is None:
            raise _CUSTOM_ERRORS.NoCategoryFound

        for cat in raw_categories_list:
            url = cat.find("a")["href"]

            # Ignore main <li> tag
            if "books_1" in url:
                continue

            name = cat.get_text().strip()

            self.library.create_category(name=name, url=self.website_url + url)

            # Breaking after first cat is scrapped
            # for dev purposes
            break
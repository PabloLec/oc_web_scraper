import requests
import yaml

from pathlib import Path
from bs4 import BeautifulSoup

from oc_web_scraper import errors as _CUSTOM_ERRORS

from oc_web_scraper.saver import Saver
from oc_web_scraper.library import Library


class Handler:
    def __init__(self, website_url: str):
        self.website_url = website_url
        self.library = Library()
        self.saver = Saver()
        self.config = None

        self.scrap_homepage()

        self.saver.save_library(self.library)

    def scrap_homepage(self):
        raw_response = requests.get(self.website_url)
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

import requests

from bs4 import BeautifulSoup


class Handler:
    def __init__(self, website_url: str):

        self.website_url = website_url
        self.library = None

    def create_library(self):
        self.library = Library

    def scrap_homepage(self):
        raw_response = requests.get(self.website_url)

        soup = BeautifulSoup(raw_response.content, "html.parser")

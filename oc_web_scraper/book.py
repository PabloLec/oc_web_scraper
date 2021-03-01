import requests
import re

from bs4 import BeautifulSoup

from oc_web_scraper import errors as _CUSTOM_ERRORS


class Book:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url
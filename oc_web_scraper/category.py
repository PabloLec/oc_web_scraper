import requests
import re

from bs4 import BeautifulSoup

from oc_web_scraper import errors as _CUSTOM_ERRORS
from oc_web_scraper.book import Book


class Category:
    def __init__(self, name: str, url: str):

        self.number_of_books_per_page = 20
        self.book_relative_path = "../../../"
        self.book_absolute_path = "https://books.toscrape.com/catalogue/"

        self.name = name
        self.url = url
        self.books = {}
        self.number_of_books = 0

        self.scrap_category()

    def create_book(self, title: str, url: str):
        book_object = Book(title=title, url=url)
        self.books[title] = book_object

    def scrap_category(self):
        raw_response = requests.get(self.url)
        soup = BeautifulSoup(raw_response.content, "html.parser")

        # Scrap number of results for this category in order to avoid useless
        # GET requests later.
        nb_of_results = soup.find("form", attrs={"class": "form-horizontal"})

        if nb_of_results is None:
            raise _CUSTOM_ERRORS.NoResultFoundForCategory(self.url)

        results_text = nb_of_results.get_text()

        self.number_of_books = int(re.findall("([0-9]+) results", results_text)[0])

        if self.number_of_books <= self.number_of_books_per_page:
            self.scrap_category_page(self.url)
        else:
            number_of_pages = (
                self.number_of_books // self.number_of_books_per_page
            ) + 1
            for page_number in range(1, number_of_pages + 1):
                page_url = self.url.replace(
                    "index", "page-{num}".format(num=page_number)
                )
                self.scrap_category_page(page_url)

    def scrap_category_page(self, url: str):
        raw_response = requests.get(self.url)
        soup = BeautifulSoup(raw_response.content, "html.parser")

        books_titles = soup.find_all("h3")

        for book in books_titles:
            url = book.find("a")["href"]
            absolute_url = url.replace(self.book_relative_path, self.book_absolute_path)
            book_title = book.find("a")["title"].strip()

            self.create_book(title=book_title, url=absolute_url)
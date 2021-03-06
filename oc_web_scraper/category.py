import re
import requests

from bs4 import BeautifulSoup

from oc_web_scraper import errors as _CUSTOM_ERRORS
from oc_web_scraper.logger import Logger
from oc_web_scraper.book import Book


class Category:
    """Category class manages category page scraping,
    stores its information and its associated books in
    a dict. Also, instantiate Book objects during scraping.

    Attributes:
        logger (Logger): Main app logger object. Passed in instantiation arguments.
        number_of_books_per_page (int): Number of books per page displayed
        by the website.
        book_relative_path (str): Relative path hard-coded in book pages URLs.
        book_absolute_path (str): Absolute equivalent of the relative path.
        name (str): Category name. Passed in instantiation arguments.
        url (str): Category page URL. Passed in instantiation arguments.
        books (dict): Books scrapped in the category page(s).
        Format is "book_title": Book object.
        number_of_books (int): Number of books associated with the category.
        Provided by a string in page source.
    """

    def __init__(self, name: str, url: str, logger: Logger):
        """Constructor for Category class.

        Args:
            name (str): Category name.
            url (str): Category page URL.
            logger (Logger): Main app logger object.
        """

        self.logger = logger

        # Number of books per page displayed by the website and book
        # pages URL relative part and its absolute equivalent
        # are hard coded to ease eventual adaptation for
        # future website structure modifications.
        self.number_of_books_per_page = 20
        self.book_relative_path = "../../../"
        self.book_absolute_path = "https://books.toscrape.com/catalogue/"

        self.name = name
        self.url = url

        self.books = {}
        self.number_of_books = 0

        self.logger.write(
            log_level="info",
            message="Created category named '{name}'. Starting scraping process...".format(
                name=self.name
            ),
        )

        self.scrap_category()

        self.logger.write(
            log_level="info",
            message="{scrapped_num}/{website_num} book(s) scrapped for category.".format(
                scrapped_num=len(self.books),
                website_num=self.number_of_books,
            ),
        )

    def __str__(self):
        stdout_content = " - Name: {name}\n".format(name=self.name)
        stdout_content += "  - URL: {url}\n\n".format(url=self.url)
        stdout_content += "  - Number of books (provided by website): {num}\n".format(
            num=self.number_of_books
        )
        stdout_content += "  - Number of books (scrapped): {num}\n".format(
            num=len(self.books)
        )

        return stdout_content

    def create_book(self, title: str, url: str):
        """Instantiate a Book object with previously scrapped infos.

        Args:
            title (str): Book title.
            url (str): Book page URL.
        """

        book_object = Book(title=title, url=url, category=self.name, logger=self.logger)
        self.books[title] = book_object

    def scrap_category(self):
        """Scraping process for default category page.
        Calls scrap_category_page function for proper scraping
        per page.
        """

        soup = self.create_soup()

        self.find_number_of_books_to_scrap(soup=soup)

        # If number of pages is greater than number displayed per
        # page, handle multiple pages scraping.
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

    def create_soup(self):
        """Create a BeautifulSoup object from raw request response.

        Raises:
            _CUSTOM_ERRORS.CouldNotGetCategoryPage: If response code is
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
            raise _CUSTOM_ERRORS.CouldNotGetCategoryPage(url=self.url)

        self.logger.write(
            log_level="debug",
            message="Received response for category page with status code 200.",
        )

        soup = BeautifulSoup(raw_response.content, "html.parser")

        return soup

    def find_number_of_books_to_scrap(self, soup: BeautifulSoup):
        """Scrap number of results for this category in order to avoid useless
        GET requests later.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the category page.

        Raises:
            _CUSTOM_ERRORS.NoResultFoundForCategory: If no books were found for
            this category.
        """

        nb_of_results = soup.find("form", attrs={"class": "form-horizontal"})

        if nb_of_results is None:
            self.logger.write(
                log_level="error",
                message="No book result found on category page.",
            )
            raise _CUSTOM_ERRORS.NoResultFoundForCategory(self.url)

        results_text = nb_of_results.get_text()

        self.number_of_books = int(re.findall("([0-9]+) result", results_text)[0])
        self.logger.write(
            log_level="debug",
            message="{number} book(s) to scrap for this category.".format(
                number=self.number_of_books
            ),
        )

    def scrap_category_page(self, page_url: str):
        """Scraps a category page.
        Search for books and calls crate_book to instantiate a Book object.

        Args:
            url (str): Desired page URL
        """

        raw_response = requests.get(page_url)
        soup = BeautifulSoup(raw_response.content, "html.parser")

        books_titles = soup.find_all("h3")

        for book in books_titles:
            url = book.find("a")["href"]
            absolute_url = url.replace(self.book_relative_path, self.book_absolute_path)
            book_title = book.find("a")["title"].strip()

            self.create_book(title=book_title, url=absolute_url)

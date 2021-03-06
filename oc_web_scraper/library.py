from oc_web_scraper.logger import Logger
from oc_web_scraper.category import Category


class Library:
    """Library class handles scrapping content collection and storage
    by instantiating Category objects.

    Attributes:
        logger (Logger): Main app logger object. Passed in instantiation arguments.
        categories (dict): Categories scrapped in the main website page."""

    def __init__(self, logger: Logger):
        """Constructor for Library class.

        Args:
            logger (Logger): Main app logger object.
        """

        self.logger = logger

        self.categories = {}

    def create_category(self, name: str, url: str):
        """Instantiate a Category object with scrapped infos.

        Args:
            name (str): Name of the category.
            url (str): URL of the category page.
        """

        category_object = Category(name=name, url=url, logger=self.logger)
        self.categories[name] = category_object
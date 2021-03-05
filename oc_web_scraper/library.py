from oc_web_scraper.category import Category


class Library:
    """Library class handles scrapping content collection and storage
    by instantiating Category objects."""

    def __init__(self):
        """Constructor class for Library class.

        Attributes:
            categories (dict): Categories scrapped in the main website page.
        """

        self.categories = {}

    def create_category(self, name: str, url: str):
        """Instantiate a Category object with scrapped infos

        Args:
            name (str): Name of the category.
            url (str): URL of the category page.
        """
        category_object = Category(name=name, url=url)
        self.categories[name] = category_object
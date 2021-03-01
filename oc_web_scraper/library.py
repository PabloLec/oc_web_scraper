from oc_web_scraper.category import Category


class Library:
    def __init__(self):

        self.categories = {}

    def create_category(self, name: str, url: str):
        category_object = Category(name=name, url=url)
        self.categories[name] = category_object
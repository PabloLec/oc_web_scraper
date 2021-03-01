class Category:
    def __init__(self, name: str, url: str):

        self.name = name
        self.url = url
        self.books = {}

        print(url, name)

    def create_book(self):
        pass

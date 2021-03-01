class NoCategoryContainerFound(Exception):
    """Raised when category container is not found during scraping"""

    def __init__(self):
        super().__init__("No category container found in main page.")


class NoCategoryFound(Exception):
    """Raised when no category were found in container"""

    def __init__(self):
        super().__init__("No category found within main page's container.")


class NoResultFoundForCategory(Exception):
    """Raised when no category were found in container"""

    def __init__(self, url):
        super().__init__(
            "No result were found for this category. Verify the validity of given url: \n{url}".format(
                url=url
            )
        )

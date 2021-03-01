class NoCategoryContainerFound(Exception):
    """Raised when category container is not found during scraping"""

    def __init__(self):
        super().__init__("No category container found in main page.")


class NoCategoryFound(Exception):
    """Raised when no category were found in container"""

    def __init__(self):
        super().__init__("No category found within main page's container.")


class NoResultFoundForCategory(Exception):
    """Raised when no results are found for given category page"""

    def __init__(self, url: str):
        super().__init__(
            "No result were found for this category. Verify the validity of given url: \n{url}".format(
                url=url
            )
        )


class BookInfoParsingFailed(Exception):
    """Raised when some info were not found within book info container"""

    def __init__(self, title: str):
        super().__init__("Failed to parse infos for book: {title}.".format(title=title))


class NoImageFound(Exception):
    """Raised when no image is found on given book page"""

    def __init__(self, title: str):
        super().__init__(
            "No product image found for book: {title}.".format(title=title)
        )


class NoRatingFound(Exception):
    """Raised when no rating is found on given book page"""

    def __init__(self, title: str):
        super().__init__(
            "No product rating found for book: {title}.".format(title=title)
        )


class FailedToGetRating(Exception):
    """Raised when unable to parse rating from class attributes"""

    def __init__(self, attributes: list):
        super().__init__(
            "Failed to parse rating with attributes: {attrs}.".format(
                attrs=str(attributes)
            )
        )


class NoProductDescriptionFound(Exception):
    """Raised when no description is found on given book page"""

    def __init__(self, title: str):
        super().__init__(
            "No product description found for book: {title}.".format(title=title)
        )


class NoProductInformationFound(Exception):
    """Raised when no information is found on given book page"""

    def __init__(self, title: str):
        super().__init__(
            "No product information found for book: {title}.".format(title=title)
        )


class CouldNotParseInfo(Exception):
    """Raised when no information is found on given book page"""

    def __init__(self, title: str, info: str):
        super().__init__(
            "Could not parse {info} for title: {title}.".format(info=info, title=title)
        )
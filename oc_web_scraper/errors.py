class CouldNotGetMainPage(Exception):
    """Raised when status code for main page GET request is different from 200."""

    def __init__(self, url):
        super().__init__(
            "Could not get the main page. Verify your website URL.\nURL: {url}".format(
                url=url
            )
        )


class SavePathDoesNotExists(Exception):
    """Raised when path provided in config for saving does not exists."""

    def __init__(self, path):
        super().__init__(
            "Save path does not exists. Verify your config file.\nCurrent path: {path}".format(
                path=path
            )
        )


class CouldNotParseLogLevel(Exception):
    """Raised when log level provided in config is not recognized."""

    def __init__(self, level):
        super().__init__(
            "Could not parse log level provided in config.yml file.\nValue: {level}".format(
                level=level
            )
        )


class NoCategoryContainerFound(Exception):
    """Raised when category container is not found during scraping"""

    def __init__(self):
        super().__init__("No category container found in main page.")


class NoCategoryFound(Exception):
    """Raised when no category were found in container"""

    def __init__(self):
        super().__init__("No category found within main page's container.")


class CouldNotGetCategoryPage(Exception):
    """Raised when status code for cat page GET request is different from 200."""

    def __init__(self, url):
        super().__init__(
            "Could not get the category page. Verify URL.\nURL: {url}".format(url=url)
        )


class NoResultFoundForCategory(Exception):
    """Raised when no results are found for given category page"""

    def __init__(self, url: str):
        super().__init__(
            "No result were found for this category. Verify the validity of given url: \n{url}".format(
                url=url
            )
        )


class CouldNotGetBookPage(Exception):
    """Raised when status code for book page GET request is different from 200."""

    def __init__(self, url):
        super().__init__(
            "Could not get the book page. Verify URL.\nURL: {url}".format(url=url)
        )


class BookInfoParsingFailed(Exception):
    """Raised when some info were not found within book info container"""

    def __init__(self, title: str, url: str):
        super().__init__(
            "Failed to parse infos for book: {title}.\nURL: {url}".format(
                title=title, url=url
            )
        )


class NoImageFound(Exception):
    """Raised when no image is found on given book page"""

    def __init__(self, title: str, url: str):
        super().__init__(
            "No product image found for book: {title}.\nURL: {url}".format(
                title=title, url=url
            )
        )


class NoRatingFound(Exception):
    """Raised when no rating is found on given book page"""

    def __init__(self, title: str, url: str):
        super().__init__(
            "No product rating found for book: {title}.\nURL: {url}".format(
                title=title, url=url
            )
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
    """Raised when description is found on given book page contained
    text is not."""

    def __init__(self, title: str, url: str):
        super().__init__(
            "No product description found for book: {title}.\nURL: {url}".format(
                title=title, url=url
            )
        )


class NoProductInformationFound(Exception):
    """Raised when no information is found on given book page"""

    def __init__(self, title: str, url: str):
        super().__init__(
            "No product information found for book: {title}.\nURL: {url}".format(
                title=title, url=url
            )
        )


class CouldNotParseInfo(Exception):
    """Raised when no information is found on given book page"""

    def __init__(self, title: str, info: str, url: str):
        super().__init__(
            "Could not parse {info} for title: {title}.\nURL: {url}".format(
                info=info, title=title, url=url
            )
        )


class FailedToSaveImage(Exception):
    """Raised when bad response code is returned from Image URL GET request"""

    def __init__(self, title: str, url: str):
        super().__init__(
            "Could get image for title: {title}.\nURL: {url}".format(
                title=title, url=url
            )
        )
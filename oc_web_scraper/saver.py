from pathlib import Path

from oc_web_scraper import errors as _CUSTOM_ERRORS

_SAVE_PATH = "/tmp/"


def save_path_exists(save_path: str):
    path_object = Path(save_path)

    if not path_object.exists():
        raise _CUSTOM_ERRORS.SavePathDoesNotExists(save_path)

    return True


# Add a function to check whether csv file already exists or not.
# If so create a .csv.backup file


def save_library(library):
    pass
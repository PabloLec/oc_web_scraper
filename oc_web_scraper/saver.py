import csv

from pathlib import Path, PurePath

from oc_web_scraper import errors as _CUSTOM_ERRORS
from oc_web_scraper.library import Library

_SAVE_PATH = "/tmp/"

# Format:
# data/NomDelaCategory/NomDelaCategory.csv
# data/NomDelaCategory/Image/TitreDulivre.jpg


def save_path_exists(save_path: str):
    path_object = Path(save_path)

    if not path_object.exists():
        raise _CUSTOM_ERRORS.SavePathDoesNotExists(save_path)

    return True


# Add a function to check whether csv file already exists or not.
# If so create a .csv.backup file


def save_library(library: Library, save_path: str):
    path_object = Path(save_path)

    for category in library.categories:
        print(category)
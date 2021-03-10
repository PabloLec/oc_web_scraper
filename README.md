# oc_web_scraper [![GitHub](https://img.shields.io/github/license/pablolec/oc_web_scraper)](https://github.com/PabloLec/oc_web_scraper/blob/main/LICENCE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

:books: Made for an [OpenClassrooms](https://openclassrooms.com) studies project.

oc_web_scraper scrapes a [dummy book store website](https://books.toscrape.com/) and saves its entire library locally.

## Installation

#### :penguin: Linux / :apple: macOS

```bash
git clone https://github.com/pablolec/oc_web_scraper
cd oc_web_scraper
python3 -m venv env
source env/bin/activate
pip install .
```

#### :framed_picture: Windows 

```powershell
git clone https://github.com/pablolec/oc_web_scraper
cd oc_web_scraper
py -m venv env
.\env\Scripts\activate
pip install .
```

## Usage

**Before execution**, make sure to review `config.yml` to set the scraping content save path. You may also custom the logging behavior.

#### :penguin: Linux / :apple: macOS

```bash
python3 -m oc_web_scraper
```

#### :framed_picture: Windows 

```powershell
py oc_web_scraper
```

_:floppy_disk: The website content will be saved into a folder named `data`. Subfolders will be created per category with corresponding books infos inside a csv file and book cover images stored under `data/CATEGORY_NAME/images/`._

## Improvement

As the MIT Licence once said, the software is provided 'as is'. Being a study project for a particular website, its usage can hardly be extended.

:bulb: Although, performances and UX could be enhanced by:

- Multithreading with creating a pool of either individual GET requests or whole category scrapes.
- Including date/time in dir and file naming. It would ease periodical scraping.
- Incremental saving, as the whole process takes several minutes it could be useful to prevent data loss.
- Comparing scraped results with previously-stored results to bring relevant changes to user attention.

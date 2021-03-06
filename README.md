# oc_web_scraper [![GitHub](https://img.shields.io/github/license/pablolec/oc_web_scraper)](https://github.com/PabloLec/oc_web_scraper/blob/main/LICENCE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Made for an [OpenClassrooms](https://openclassrooms.com) studies project.

oc_web_scraper scrapes a [dummy book store website](https://books.toscrape.com/) and saves its entire library locally.

## Installation

```bash
git clone https://github.com/pablolec/oc_web_scraper
cd oc_web_scraper
pip install .
```

## Usage

Before execution, make sure to review `config.yml` to set the scraping content save path. You may also custom the logging behavior.

Then, simply type `oc_web_scraper` and the scraping process will start.

The website content will be saved locally to a folder named `data`. Subfolders will be created per category with corresponding books infos in a csv file and book cover images stored in `data/CATEGORY_NAME/images/`.

## Improvement

As the MIT Licence once said, the software is provided 'as is'. Being a study project for a particular website, its usage can hardly be extended.

Although, performances and UX could be enhanced by:

- Multithreading with creating a pool of either individual GET requests or whole category scrapes.
- Including date/time in dir and file naming. It would ease periodical scraping.
- Incremental saving, as the whole process takes several minutes it could be useful to prevent data loss.
- Comparing scraped results with previously-stored results to bring relevant changes to user attention.

import requests

from bs4 import BeautifulSoup

from oc_web_scraper.handler import Handler


def main():
    Handler("https://books.toscrape.com/") b
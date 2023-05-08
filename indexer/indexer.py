import requests
import logging
from util.database.database_access import DatabaseAccess
from util.scraper.detail_page import (
    get_download_url,
    get_film_actresses,
    generate_thumbnail,
    get_film_duration,
    get_film_title,
    get_iframe_source,
    get_poster,
)
from util.scraper.document import get_document
from util.scraper.list_page import collect_urls
from util.models.indexed import IndexedIn
import time
from rich import print
from beartype import beartype
import re


@beartype
def build_url(film_id: int) -> str:
    return f"https://hqporner.com/hdporn/{film_id}.html"


@beartype
def index(film_id: int) -> IndexedIn:
    url = build_url(film_id)  # build url from film_id
    document = get_document(url)  # get the document from the url

    actresses = get_film_actresses(document)
    title = get_film_title(document)

    iframe_source = get_iframe_source(document)
    iframe_document = get_document(
        iframe_source
    )  # get the document from the iframe source
    poster = get_poster(iframe_document)
    thumbnail = generate_thumbnail(poster)
    indexed: IndexedIn = IndexedIn(
        film_id=film_id,
        title=title,
        actresses=actresses,
        thumbnail=thumbnail,
        url=url,
    )
    logging.info(f"Indexed film {film_id}")
    return indexed


@beartype
def extract_film_id(url: str) -> int:
    return int(re.search("(\d+)", url).group(1))


@beartype
class Indexer:
    def __init__(self, databaseAccess: DatabaseAccess, *, sleep_time: int = 15, iterator_sleep_time: int = 1):
        self.db = databaseAccess
        self.sleep_time = sleep_time
        self.iterator_sleep_time = iterator_sleep_time

    def main_loop(
        self,
    ):
        while True:
            """
            Once every hour:
                1. get all urls from the first page of the site
                2. for each url:
                    2.1. parse the url and get the film_id
                    2.2. check if the film_id is already in the database
                    2.3. if it is not, begin indexing
                3. wait for an hour
            """
            
            urls: list[str] = collect_urls(
                get_document("https://hqporner.com/hdporn/1")
            )

            for url in urls:
                time.sleep(self.iterator_sleep_time)
                film_id: int = extract_film_id(url)
                if not self.db.is_indexed(film_id):
                    self.db.insert_indexed(index(film_id))
                else:
                    logging.info(f"Film {film_id} already indexed. Skipping.")
            logging.info("Sleeping for 15 seconds...")
            time.sleep(self.sleep_time)
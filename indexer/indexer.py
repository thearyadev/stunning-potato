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


def build_url(film_id: int) -> str:
    return f"https://hqporner.com/hdporn/{film_id}.html"


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

    return IndexedIn(
        film_id=film_id,
        title=title,
        actresses=actresses,
        thumbnail=thumbnail,
        url=url,
    )


class Indexer:
    def __init__(self, databaseAccess: DatabaseAccess):
        self.db = databaseAccess
        print(collect_urls(get_document("https://hqporner.com/")))

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
            break

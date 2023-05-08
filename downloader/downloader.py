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

from util.database.database_access import DatabaseAccess

import logging
from beartype import beartype

@beartype
def download(url: str) -> None:
    logging.info(f"Downloading {url}")

@beartype
class Downloader:
    def __init__(self, databaseAccess: DatabaseAccess):
        self.db = databaseAccess

    def main_loop():
        ...
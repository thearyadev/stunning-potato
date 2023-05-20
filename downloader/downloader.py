import logging
import os
import time
import urllib.request
from pathlib import Path
from uuid import UUID

import requests
from beartype import beartype

from util.database.database_access import DatabaseAccess
from util.models.film import Film, FilmStateEnum
from util.models.queue import Queue
from util.scraper.detail_page import get_download_url, get_iframe_source
from util.scraper.document import get_document


@beartype
class Downloader:
    def __init__(self, databaseAccess: DatabaseAccess):
        self.db = databaseAccess
        self.download_path = Path(os.getenv("DOWNLOAD_PATH"))
        self.last_reported_progress = None

    def main_loop(self):
        while True:
            queue_item: Queue = self.db.get_and_pop_queue()  # get and pop from queue
            if queue_item is not None:
                film: Film = self.db.get_film(queue_item.film_uuid)  # get film

                # get download url
                self.db.set_film_state(
                    film.uuid, new_state=FilmStateEnum.DOWNLOADING
                )  # set_state to DOWNLOADING
                self.download(
                    get_download_url(
                        get_document(get_iframe_source(get_document(queue_item.url)))
                    ),
                    film,
                )  # begin downloading
                # complete download
                self.db.set_film_state(
                    queue_item.film_uuid, new_state=FilmStateEnum.COMPLETE
                )  # set_state to COMPLETE
            time.sleep(5)

    def download(self, url: str, film: Film) -> None:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        download_size = 0
        last_reported_progress = 0
        with open(Path(os.getenv("DOWNLOAD_PATH")).joinpath(film.filename), "wb") as f:
            for data in response.iter_content(chunk_size=4096):
                download_size += len(data)
                f.write(data)
                f.flush()
                progress = int((download_size / total_size) * 100)
                if progress != last_reported_progress:
                    self.db.set_film_progress(newProgress=progress, film_uuid=film.uuid)
                    last_reported_progress = progress

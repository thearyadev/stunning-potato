from util.scraper.detail_page import (
    get_download_url,
    get_iframe_source,
)
from util.scraper.document import get_document

from util.database.database_access import DatabaseAccess
import time
from util.models.film import FilmStateEnum, Film
from util.models.queue import Queue

import logging
from beartype import beartype
import urllib.request
import os
from pathlib import Path
from uuid import UUID


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
        def report_hook(count: int, block_size: int, total_size: int):
            progress: int = int(count * block_size * 100 / total_size)
            if progress % 10 == 0 and progress != self.last_reported_progress:
                self.last_reported_progress = progress
                print(f"{progress}%")

        fname = rf"{self.download_path}/{film.filename}"
        urllib.request.urlretrieve(
            url,
            r"F:\temp_downloads\test.mp4",
            reporthook=report_hook,
        )

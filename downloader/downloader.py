from util.scraper.detail_page import (
    get_download_url,
    get_iframe_source,
)
from util.scraper.document import get_document

from util.database.database_access import DatabaseAccess
import time
from util.models.film import FilmStateEnum

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

    def main_loop(self):
        while True:
            queue_item = self.db.get_and_pop_queue()  # get and pop from queue
            if queue_item is not None:
                # get download url
                self.db.set_film_state(
                    queue_item.film_uuid, new_state=FilmStateEnum.DOWNLOADING
                )  # set_state to DOWNLOADING
                self.download(
                    get_download_url(
                        get_document(get_iframe_source(get_document(queue_item.url)))
                    ),
                    os.path.join(self.download_path, f"this is a uuid.mp4"),
                )  # begin downloading
                # complete download
                self.db.set_film_state(
                    queue_item.film_uuid, new_state=FilmStateEnum.COMPLETE
                )  # set_state to COMPLETE
            time.sleep(5)

    

    def download(self, url: str, filename, uuid: UUID) -> None:

        def report_hook(count: int, block_size: int, total_size: int):
            # tells db to do the thing
            progress: float = count * block_size * 100 / total_size
            if progress % 25 == 0:
                # self.db.set_film_progress(uuid, progress)
                ...

        urllib.request.urlretrieve(url, filename, reporthook=report_hook)

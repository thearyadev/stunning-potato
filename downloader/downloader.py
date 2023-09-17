import logging
import os
import time
import urllib.request
from pathlib import Path
from uuid import UUID

import ffmpeg
import requests
import whisper
from beartype import beartype
from whisper.utils import WriteVTT

from util.database.database_access import DatabaseAccess
from util.models.film import Film, FilmStateEnum
from util.models.queue import Queue
from util.scraper.detail_page import get_download_url, get_iframe_source
from util.scraper.document import get_document


# @beartype
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
                self.db.set_film_state(
                    queue_item.film_uuid, new_state=FilmStateEnum.TRANSCODING
                )
                self.transcode(film)  # transcode
                self.transcribe(film)  # transcribe
                # complete process
                self.db.set_film_state(
                    queue_item.film_uuid, new_state=FilmStateEnum.COMPLETE
                )  # set_state to COMPLETE
            time.sleep(5)

    def transcode(self, film: Film) -> bool:
        """
        Transcodes a film from the given path to the given path.

        Args:
            film (Film): The Film object representing the file to transcode.

        Returns:
            None
        """
        target_path: Path = Path(os.getenv("DOWNLOAD_PATH")).joinpath(film.filename)
        output_path: Path = Path(os.getenv("DOWNLOAD_PATH")).joinpath(
            f"{film.filename}.transcoding.mp4"
        )
        logging.info(f"Transcoding {target_path} to {output_path}")
        try:
            ffmpeg.input(target_path).output(
                str(output_path),
                vcodec="libx264",
                video_bitrate="1750k",
                acodec="aac",
                strict="experimental",
                ab="192k",
                movflags="faststart",
                threads=1,
            ).run()

        except Exception as e:
            logging.error(f"Transcoding failed for {target_path}")
            logging.error(e)
            return False

        logging.info(f"Transcoding complete for {target_path}")
        target_path.unlink()
        output_path.rename(target_path)
        return True

    def transcribe(self, film: Film) -> bool:
        """
        Transcribes a film from the given path to the given path.

        Args:
            film (Film): The Film object representing the file to transcribe.

        Returns:
            None
        """
        os.environ["XDG_CACHE_HOME"] = "./.cache"
        model = whisper.load_model("tiny")
        target_path: Path = Path(os.getenv("DOWNLOAD_PATH")).joinpath(film.filename)
        output_path: Path = (
            Path(os.getenv("SUBTITLES_PATH"))
            .joinpath(film.filename)
            .with_suffix(".vtt")
        )
        logging.info(f"Transcribing {target_path} to {output_path}")
        try:
            result = model.transcribe(
                str(target_path), initial_prompt="porn, sex, moan"
            )
            with output_path.open("w") as vtt_file:
                WriteVTT(".").write_result(result, vtt_file)
        except Exception as e:
            logging.error(f"Transcribing failed for {target_path}")
            logging.error(e)
            if output_path.exists():
                output_path.unlink()
            return False
        return True

    def download(self, url: str, film: Film) -> None:
        """
        Downloads a file from the given URL and saves it to disk, while reporting progress to the database.

        Args:
            url (str): The URL of the file to download.
            film (Film): The Film object representing the file to download.

        Returns:
            None
        """

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

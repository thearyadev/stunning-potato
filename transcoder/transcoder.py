import ffmpeg
from beartype import beartype

from util.database.database_access import DatabaseAccess


@beartype
def encode() -> None:
    ...


@beartype
def transcribe() -> None:
    ...


@beartype
class Transcoder:
    def __init__(
        self,
        databaseAccess: DatabaseAccess,
        *,
        sleep_time: int = 1800,
        iterator_sleep_time: int = 5,
    ):
        self.db = databaseAccess
        self.sleep_time = sleep_time
        self.iterator_sleep_time = iterator_sleep_time

    def main_loop(
        self,
    ):
        raise NotImplementedError
        while True:
            ...

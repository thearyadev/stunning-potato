from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from uuid import UUID


class FilmStateEnum(str, Enum):
    DOWNLOADING = "DOWNLOADING"
    IN_QUEUE = "IN QUEUE"
    COMPLETE = "COMPLETE"


@dataclass
class FilmIn:
    title: str
    duration: timedelta
    date_added: date
    filename: str
    watched: bool
    state: FilmStateEnum
    actresses: list[str]
    rating: UUID

    thumbnail: bytes
    poster: bytes
    download_progress: int

    def __repr__(
        self,
    ) -> str:
        return (
            "FilmIn(title=%s, duration=%s, date_added=%s, filename=%s, watched=%s, state=%s,"
            "actresses=%s, rating=%s, download_progress=%s)"
            % (
                self.title,
                self.duration,
                self.date_added,
                self.filename,
                self.watched,
                self.state,
                self.actresses,
                self.rating,
                self.download_progress,
            )
        )


@dataclass
class Film:
    uuid: UUID
    title: str
    duration: timedelta
    date_added: date
    filename: str
    watched: bool
    state: FilmStateEnum
    actresses: list[str]
    rating: UUID

    thumbnail: bytes | memoryview
    poster: bytes | memoryview
    download_progress: int

    def __repr__(
        self,
    ) -> str:
        return (
            "Film(uuid=%s, title=%s, duration=%s, date_added=%s, filename=%s, watched=%s, state=%s,"
            "actresses=%s, rating=%s, download_progress=%s)"
            % (
                self.uuid,
                self.title,
                self.duration,
                self.date_added,
                self.filename,
                self.watched,
                self.state,
                self.actresses,
                self.rating,
                self.download_progress,
            )
        )


@dataclass
class FilmNoBytes:
    uuid: UUID
    title: str
    duration: timedelta
    date_added: date
    filename: str
    watched: bool
    state: FilmStateEnum
    actresses: list[str]
    rating: UUID
    download_progress: int

    def __repr__(
        self,
    ) -> str:
        return (
            "FilmNoBytes(uuid=%s, title=%s, duration=%s, date_added=%s, filename=%s, watched=%s, state=%s,"
            "actresses=%s, rating=%s, download_progress=%s)"
            % (
                self.uuid,
                self.title,
                self.duration,
                self.date_added,
                self.filename,
                self.watched,
                self.state,
                self.actresses,
                self.rating,
                self.download_progress,
            )
        )


@dataclass
class FilmNoBytesWithAverage:
    uuid: UUID
    title: str
    duration: timedelta
    date_added: date
    filename: str
    watched: bool
    state: FilmStateEnum
    download_progress: int
    actresses: list[str]
    rating: UUID
    average: float

    def __repr__(
        self,
    ) -> str:
        return (
            "FilmNoBytesWithAverage(uuid=%s, title=%s, duration=%s, date_added=%s, filename=%s, watched=%s, state=%s,"
            "actresses=%s, rating=%s, download_progress=%s, average=%s)"
            % (
                self.uuid,
                self.title,
                self.duration,
                self.date_added,
                self.filename,
                self.watched,
                self.state,
                self.actresses,
                self.rating,
                self.download_progress,
                self.average,
            )
        )

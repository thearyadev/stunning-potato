from datetime import date, timedelta
from enum import Enum
from uuid import UUID

from dataclasses import dataclass


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

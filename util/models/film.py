from datetime import date, datetime, time, timedelta
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, validator


class FilmStateEnum(str, Enum):
    DOWNLOADING = "DOWNLOADING"
    IN_QUEUE = "IN QUEUE"
    COMPLETE = "COMPLETE"


class FilmIn(BaseModel):
    title: str = Field(alias="title")
    duration: timedelta = Field(alias="duration")
    date_added: date = Field(alias="date_added")
    filename: str = Field(alias="filename")
    watched: bool = Field(alias="watched")
    state: FilmStateEnum = Field(alias="state")
    actresses: list[str] = Field(alias="actresses")
    rating: UUID = Field(alias="rating")

    thumbnail: bytes = Field(alias="thumbnail")
    poster: bytes = Field(alias="poster")
    download_progress: int = Field(alias="download_progress")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            timedelta: lambda v: str(v),
            date: lambda v: v.isoformat(),
            bytes: lambda _: None,
        }


class Film(BaseModel):
    uuid: UUID = Field(alias="uuid")
    title: str = Field(alias="title")
    duration: timedelta = Field(alias="duration")
    date_added: date = Field(alias="date_added")
    filename: str = Field(alias="filename")
    watched: bool = Field(alias="watched")
    state: FilmStateEnum = Field(alias="state")
    actresses: list[str] = Field(alias="actresses")
    rating: UUID = Field(alias="rating")


    thumbnail: bytes = Field(alias="thumbnail")
    poster: bytes = Field(alias="poster")
    download_progress: int = Field(alias="download_progress")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            timedelta: lambda v: str(v),
            date: lambda v: v.isoformat(),
            bytes: lambda _: None,
        }

    @validator("thumbnail", "poster", pre=True)
    def convert_memoryview(cls, value):
        if isinstance(value, memoryview):
            return bytes(value)
        return value


class FilmNoBytes(BaseModel):
    uuid: UUID = Field(alias="uuid")
    title: str = Field(alias="title")
    duration: timedelta = Field(alias="duration")
    date_added: date = Field(alias="date_added")
    filename: str = Field(alias="filename")
    watched: bool = Field(alias="watched")
    state: FilmStateEnum = Field(alias="state")
    download_progress: int = Field(alias="download_progress")
    actresses: list[str] = Field(alias="actresses")
    rating: UUID = Field(alias="rating")

class FilmNoBytesWithAverage(BaseModel):
    uuid: UUID = Field(alias="uuid")
    title: str = Field(alias="title")
    duration: timedelta = Field(alias="duration")
    date_added: date = Field(alias="date_added")
    filename: str = Field(alias="filename")
    watched: bool = Field(alias="watched")
    state: FilmStateEnum = Field(alias="state")
    download_progress: int = Field(alias="download_progress")
    actresses: list[str] = Field(alias="actresses")
    rating: UUID = Field(alias="rating")
    average: float = Field(alias="average")


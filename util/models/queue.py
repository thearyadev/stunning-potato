from uuid import UUID

from pydantic import BaseModel, Field


class QueueIn(BaseModel):
    url: str
    film_uuid: UUID = Field(alias="film_uuid")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Queue(BaseModel):
    uuid: UUID = Field(alias="uuid")
    url: str = Field(alias="url")
    film_uuid: UUID = Field(alias="film_uuid")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

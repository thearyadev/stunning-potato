from uuid import UUID

from pydantic import BaseModel, Field


# junction table
class FilmActressRating(BaseModel):
    uuid: UUID = Field(alias="uuid")
    film_uuid: UUID = Field(alias="film_uuid")
    actress_uuid: list[UUID] = Field(alias="actress_uuid")
    rating_uuid: UUID = Field(alias="rating_uuid")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FilmActressRatingIn(BaseModel):
    film_uuid: UUID = Field(alias="film_uuid")
    actress_uuid: list[UUID] = Field(alias="actress_uuid")
    rating_uuid: UUID = Field(alias="rating_uuid")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

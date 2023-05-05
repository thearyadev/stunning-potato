from uuid import UUID

from pydantic import BaseModel, Field, validator


class IndexedIn(BaseModel):
    title: str = Field(alias="title")
    actresses: list[str] = Field(alias="actresses")
    thumbnail: bytes = Field(alias="thumbnail")
    url: str = Field(alias="url")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Indexed(BaseModel):
    uuid: UUID = Field(alias="uuid")
    title: str = Field(alias="title")
    actresses: list[str] = Field(alias="actresses")
    thumbnail: bytes = Field(alias="thumbnail")
    url: str = Field(alias="url")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @validator("thumbnail", pre=True)
    def convert_memoryview(cls, value):
        if isinstance(value, memoryview):
            return bytes(value)
        return value


class IndexedNoBytes(BaseModel):
    uuid: UUID = Field(alias="uuid")
    title: str = Field(alias="title")
    actresses: list[str] = Field(alias="actresses")
    url: str = Field(alias="url")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

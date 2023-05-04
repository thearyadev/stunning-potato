from pydantic import BaseModel, Field

class IndexedIn(BaseModel):
    title: str = Field(alias="title")
    actresses: list[str] = Field(alias="actresses")
    thumbnail: bytes = Field(alias="thumbnail")
    url: str = Field(alias="url")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        
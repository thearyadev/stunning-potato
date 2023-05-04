from pydantic import BaseModel, validator, Field
from uuid import UUID


class RatingIn(BaseModel):
    story: int = Field(ge=0, le=10, alias="story")
    positions: int = Field(ge=0, le=10, alias="positions")
    pussy: int = Field(ge=0, le=10, alias="pussy")
    shots: int = Field(ge=0, le=10, alias="shots")
    boobs: int = Field(ge=0, le=10, alias="boobs")
    face: int = Field(ge=0, le=10, alias="face")
    rearview: int = Field(ge=0, le=10, alias="rearview")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Rating(BaseModel):
    uuid: UUID = Field(alias="uuid")

    average: float | None = Field(ge=0, le=10, alias="average")
    story: int = Field(ge=0, le=10, alias="story")
    positions: int = Field(ge=0, le=10, alias="positions")
    pussy: int = Field(ge=0, le=10, alias="pussy")
    shots: int = Field(ge=0, le=10, alias="shots")
    boobs: int = Field(ge=0, le=10, alias="boobs")
    face: int = Field(ge=0, le=10, alias="face")
    rearview: int = Field(ge=0, le=10, alias="rearview")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

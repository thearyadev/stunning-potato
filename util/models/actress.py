from uuid import UUID

from pydantic import BaseModel, validator


class ActressIn(BaseModel):
    name_: str

    @validator("name_")
    def name_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("Name must not be empty")
        return v

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Actress(BaseModel):
    uuid: UUID
    name_: str

    class Config:
        orm_mode = True

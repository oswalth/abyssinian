from datetime import datetime
from uuid import UUID

from pydantic.main import BaseModel
from humps.camel import case


def to_camel(value: str) -> str:
    return case(value)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class UidSchema(CamelModel):
    id: UUID


class CreatedAtSchema(CamelModel):
    created_at: datetime


class UpdatedAtSchema(CamelModel):
    updated_at: datetime


class BaseSchema(UidSchema, CreatedAtSchema, UpdatedAtSchema):
    pass

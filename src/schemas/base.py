from datetime import datetime
from uuid import UUID

from pydantic.main import BaseModel


class UidSchema(BaseModel):
    id: UUID


class CreatedAtSchema(BaseModel):
    created_at: datetime


class UpdatedAtSchema(BaseModel):
    updated_at: datetime


class BaseSchema(UidSchema, CreatedAtSchema, UpdatedAtSchema):
    pass

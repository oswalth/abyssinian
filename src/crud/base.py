from typing import TypeVar, Generic
from uuid import UUID

from pydantic.main import BaseModel
from sqlalchemy.orm import Session

from models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
IDType = UUID | int


class BaseCRUD(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id_: IDType) -> ModelType:
        return db.query(self.model).filter(self.model.id == id_).first()

    def get_many(self, db: Session, limit: int = 100, offset: int = 0) -> list[ModelType]:
        return db.query(self.model).order_by(self.model.id).offset(offset).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

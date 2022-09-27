from typing import TypeVar, Generic, Literal
from uuid import UUID

from pydantic.main import BaseModel
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session, Query, DeclarativeMeta, InstrumentedAttribute

from models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
IDType = UUID | int
JOIN_MODELS_TYPE = set[tuple[tuple[DeclarativeMeta, InstrumentedAttribute]]]

ASC = "asc"
DESC = "desc"
SORT_TYPE = Literal[ASC, DESC]
sort_dir_mapper = {
    ASC: asc,
    DESC: desc,
}


class BaseCRUD(Generic[ModelType, CreateSchemaType]):
    QUERY_PARAMS_MAPPING = {}

    def __init__(self, model):
        self.model = model

    def _apply_filters(self, q: Query, join_models: JOIN_MODELS_TYPE, filters: dict[str, str]) -> tuple[Query, JOIN_MODELS_TYPE]:
        if filters is not None:
            for filter_lookup, value in filters.items():
                field_mapping = self.QUERY_PARAMS_MAPPING.get(filter_lookup, {})
                if filter_by := field_mapping.get("filter_by"):
                    q = q.filter(filter_by == value)
                if fields_join := field_mapping.get("join"):
                    for field_join in fields_join:
                        join_models.add(field_join)
        return q, join_models

    def _apply_sort(self, q: Query, join_models: JOIN_MODELS_TYPE, sort: str, sort_dir: str) -> tuple[Query, JOIN_MODELS_TYPE]:
        if sort is not None:
            field_mapping = self.QUERY_PARAMS_MAPPING.get(sort, {})
            if sort := field_mapping.get("sort"):
                q = q.order_by(sort_dir_mapper[sort_dir](sort))
            if fields_join := field_mapping.get("join"):
                for field_join in fields_join:
                    join_models.add(field_join)
        return q, join_models

    def _apply_search(self, q: Query, join_models: JOIN_MODELS_TYPE, search_value: str, search_lookup: str) -> tuple[Query, JOIN_MODELS_TYPE]:
        if search_value and search_lookup:
            field_mapping = self.QUERY_PARAMS_MAPPING.get(search_lookup, {})
            if search := field_mapping.get("search"):
                q = q.filter(search.ilike("{}%".format(search_value)))
            if fields_join := field_mapping.get("join"):
                for field_join in fields_join:
                    join_models.add(field_join)
        return q, join_models

    def get(self, db: Session, id_: IDType) -> ModelType:
        return db.query(self.model).filter(self.model.id == id_).first()

    def get_many(
            self,
            db: Session,
            limit: int = 100,
            offset: int = 0,
            filters: dict[str, str] = None,
            sort: str = None,
            sort_dir: str = ASC,
            search_value: str = None,
            search_lookup: str = None,
    ) -> tuple[list[ModelType], int]:
        join_models: JOIN_MODELS_TYPE = set()
        q = db.query(self.model)
        q, join_models = self._apply_filters(q, join_models, filters)
        q, join_models = self._apply_sort(q, join_models, sort, sort_dir)
        q, join_models = self._apply_search(q, join_models, search_value, search_lookup)

        if join_models:
            q = q.join(*join_models)

        return q.\
            offset(offset).\
            limit(limit).\
            all(), db.query(self.model).count()

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

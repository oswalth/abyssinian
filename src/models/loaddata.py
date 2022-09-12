from functools import lru_cache
from typing import Callable

import yaml
from sqlalchemy.orm import Session

from core.security import get_password_hash
from dependencies import get_db
from models.users import AccessCode, User, Coach, Client


FixtureItemType = dict[str, str]


get_password_hash = lru_cache(maxsize=10)(get_password_hash)


def user_password_handler(user_objects: list[FixtureItemType]) -> list[FixtureItemType]:
    for user in user_objects:
        password = user.pop("password")
        user["hashed_password"] = get_password_hash(password)
    return user_objects


loading_order = [
    {"fixture_path": "src/models/fixtures/codes.yaml", "db_model": AccessCode},
    {"fixture_path": "src/models/fixtures/coach_users.yaml", "db_model": User, "preprocessor_callback": user_password_handler},
    {"fixture_path": "src/models/fixtures/coaches.yaml", "db_model": Coach},
    {"fixture_path": "src/models/fixtures/client_users.yaml", "db_model": User, "preprocessor_callback": user_password_handler},
    {"fixture_path": "src/models/fixtures/clients.yaml", "db_model": Client},
]


class DataLoader:
    def __init__(
            self,
            fixture_path: str,
            db_model,
            db: Session,
            preprocessor_callback: Callable[[list[FixtureItemType]], FixtureItemType],
    ):
        self.fixture_path = fixture_path
        self.db_model = db_model
        self.preprocessor_callback = preprocessor_callback
        self.db = db

    def load_data(self):
        with open(self.fixture_path) as file:
            objects = yaml.load(file, Loader=yaml.FullLoader)
        if self.preprocessor_callback:
            objects = self.preprocessor_callback(objects)
        db_objects = [self.db_model(**obj) for obj in objects]
        existing_objects = self.db.query(self.db_model).filter(self.db_model.id.in_([obj.id for obj in db_objects])).all()
        existing_objects_ids = [str(existing_object.id) for existing_object in existing_objects]
        for db_object in db_objects:
            if str(db_object.id) in existing_objects_ids:
                self.db.merge(db_object)
            else:
                self.db.add(db_object)
        self.db.commit()


db_session = next(get_db())
for fixture in loading_order:
    loader = DataLoader(
        fixture_path=fixture["fixture_path"],
        db_model=fixture["db_model"],
        db=db_session,
        preprocessor_callback=fixture.get("preprocessor_callback"),
    )
    loader.load_data()

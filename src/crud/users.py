from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import get_password_hash
from crud.base import BaseCRUD
from models.users import User, Client, AccessCode, Coach
from schemas.users import ClientCreate, CoachCreate, UserCreate, AccessCodeCreate


class AccessCodeCRUD(BaseCRUD[AccessCode, AccessCodeCreate]):
    def get_code_by_name(self, db: Session, name: str) -> User:
        return db.query(AccessCode).filter(AccessCode.name == name).first()


access_code_crud = AccessCodeCRUD(AccessCode)


class UserCRUD(BaseCRUD[User, UserCreate]):
    def get_user_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate) -> User:
        db_user = User(**user.dict(exclude={"password"}), hashed_password=get_password_hash(user.password))
        return db_user


user_crud = UserCRUD(User)


class CoachCRUD(BaseCRUD[Coach, CoachCreate]):
    def create(self, db: Session, coach: CoachCreate) -> Coach:
        db_user = user_crud.create_user(coach.user)
        db_coach = Coach(
            user=db_user,
            sessions_limit_per_week=coach.sessions_limit_per_week,
        )
        db.add(db_user, db_coach)
        db.commit()
        db.refresh(db_coach)
        return db_coach


coach_crud = CoachCRUD(Coach)


class ClientCRUD(BaseCRUD[Client, ClientCreate]):
    def create(self, db: Session, client: ClientCreate) -> Client:
        if (access_code_obj := access_code_crud.get_code_by_name(db, client.access_code)) is None:
            raise HTTPException(status_code=404, detail="Access code not found")
        db_user = user_crud.create_user(client.user)
        db_client = Client(
            user=db_user,
            access_code=access_code_obj,
            is_agree_uprise_emails=client.is_agree_uprise_emails,
            is_agree_terms_conditions=client.is_agree_terms_conditions,
        )
        db.add(db_user, db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    def set_client_coach(self, db: Session, client_id: UUID, coach_id: UUID) -> Client:
        db_coach = coach_crud.get(db, coach_id)
        db_client = self.get(db, client_id)
        db_client.coach = db_coach
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client


client_crud = ClientCRUD(Client)

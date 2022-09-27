from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import get_password_hash
from crud.base import BaseCRUD
from models.users import User, Client, AccessCode, Coach
from schemas.query import ClientSortQuery, CoachSortQuery, AccessCodeSortQuery
from schemas.users import ClientCreate, CoachCreate, UserCreate, AccessCodeCreate


class AccessCodeCRUD(BaseCRUD[AccessCode, AccessCodeCreate]):
    QUERY_PARAMS_MAPPING = {
        AccessCodeSortQuery.name.name: {
            "sort": AccessCode.name,
            "search": AccessCode.name,
        },
        AccessCodeSortQuery.created_at.name: {
            "sort": AccessCode.created_at,
        },
        AccessCodeSortQuery.updated_at.name: {
            "sort": AccessCode.updated_at,
        },
        AccessCodeSortQuery.is_active.name: {
            "sort": AccessCode.is_active,
            "filter_by": AccessCode.is_active,
        },
        AccessCodeSortQuery.is_coach_session_enabled.name: {
            "sort": AccessCode.is_coach_session_enabled,
            "filter_by": AccessCode.is_coach_session_enabled,
        },
        AccessCodeSortQuery.is_communication_request_enabled.name: {
            "sort": AccessCode.is_communication_request_enabled,
            "filter_by": AccessCode.is_communication_request_enabled,
        },
        AccessCodeSortQuery.is_care_navigation_enabled.name: {
            "sort": AccessCode.is_care_navigation_enabled,
            "filter_by": AccessCode.is_care_navigation_enabled,
        },
        AccessCodeSortQuery.is_case_manager_notification_enabled.name: {
            "sort": AccessCode.is_case_manager_notification_enabled,
            "filter_by": AccessCode.is_case_manager_notification_enabled,
        },
        AccessCodeSortQuery.is_additional_session_request_enabled.name: {
            "sort": AccessCode.is_additional_session_request_enabled,
            "filter_by": AccessCode.is_additional_session_request_enabled,
        },
    }
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
    QUERY_PARAMS_MAPPING = {
        CoachSortQuery.first_name.name: {
            "join": (User,),
            "sort": User.first_name,
            "search": User.first_name,
        },
        CoachSortQuery.last_name.name: {
            "join": (User,),
            "sort": User.last_name,
            "search": User.last_name,
        },
        CoachSortQuery.email.name: {
            "join": (User,),
            "sort": User.email,
            "search": User.email,
        },
        CoachSortQuery.is_active.name: {
            "join": (User,),
            "sort": User.is_active,
            "filter_by": User.is_active,
        },
    }

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
    QUERY_PARAMS_MAPPING = {
        ClientSortQuery.first_name.name: {
            "join": (User,),
            "sort": User.first_name,
            "search": User.first_name,
        },
        ClientSortQuery.last_name.name: {
            "join": (User,),
            "sort": User.last_name,
            "search": User.last_name,
        },
        ClientSortQuery.email.name: {
            "join": (User,),
            "sort": User.email,
            "search": User.email,
        },
        ClientSortQuery.is_active.name: {
            "join": (User,),
            "sort": User.is_active,
            "filter_by": User.is_active,
        },
        ClientSortQuery.access_code.name: {
            "join": (AccessCode,),
            "sort": AccessCode.name,
            "filter_by": AccessCode.name,
        },
        ClientSortQuery.coach.name: {
            "join": (Coach, User,),
            "sort": User.first_name,
        },
    }
    def create(self, db: Session, client: ClientCreate) -> Client:
        if (access_code_obj := access_code_crud.get_code_by_name(db, client.access_code)) is None:
            raise HTTPException(status_code=404, detail="Access code not found")
        db_user = user_crud.create_user(client.user)
        db_client = Client(
            user=db_user,
            access_code=access_code_obj,
            is_agree_emails=client.is_agree_emails,
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

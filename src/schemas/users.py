from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.main import BaseModel

from schemas.base import BaseSchema, UpdatedAtSchema


class AccessCodeBase(BaseModel):
    name: str
    is_coach_session_enabled: bool
    is_communication_request_enabled: bool
    is_care_navigation_enabled: bool
    is_case_manager_notification_enabled: bool
    is_additional_session_request_enabled: bool
    coach_session_limit: int
    is_active: bool


class AccessCodeCreate(AccessCodeBase):
    pass


class AccessCode(AccessCodeBase, BaseSchema):

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    phone_number: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase, BaseSchema):
    id: UUID
    is_active: bool
    created_at: datetime
    last_login: datetime

    class Config:
        orm_mode = True


class CoachBase(BaseModel):
    sessions_limit_per_week: int


class CoachCreate(CoachBase):
    user: UserCreate


class Coach(CoachBase, UpdatedAtSchema):
    user: User

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    is_agree_uprise_emails: bool
    is_agree_terms_conditions: bool


class ClientCreate(ClientBase):
    access_code: str
    user: UserCreate


class Client(ClientBase, UpdatedAtSchema):
    access_code: AccessCode
    user: User
    coach: Optional[Coach]

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str

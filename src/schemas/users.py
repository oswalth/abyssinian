from datetime import datetime
from uuid import UUID


from schemas.base import BaseSchema, UpdatedAtSchema, CamelModel


class AccessCodeBase(CamelModel):
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


class UserBase(CamelModel):
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


class CoachBase(CamelModel):
    sessions_limit_per_week: int


class CoachCreate(CoachBase):
    user: UserCreate


class Coach(CoachBase, UpdatedAtSchema):
    user: User

    class Config:
        orm_mode = True


class ClientBase(CamelModel):
    is_agree_emails: bool
    is_agree_terms_conditions: bool


class ClientCreate(ClientBase):
    access_code: str
    user: UserCreate


class Client(ClientBase, UpdatedAtSchema):
    access_code: AccessCode
    user: User
    coach: Coach | None

    class Config:
        orm_mode = True


class TokenData(CamelModel):
    email: str


class Token(CamelModel):
    access_token: str
    token_type: str

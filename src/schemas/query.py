import enum
from typing import Literal

from fastapi import Query
from pydantic import BaseModel

from schemas.base import CamelModel
from schemas.users import Coach, Client, AccessCode


class AccessCodeSortQuery(enum.Enum):
    name = "name"
    created_at = "createdAt"
    updated_at = "updatedAt"
    is_active = "isActive"
    is_coach_session_enabled = "isCoachSessionEnabled"
    is_communication_request_enabled = "isCommunicationRequestEnabled"
    is_care_navigation_enabled = "isCareNavigationEnabled"
    is_case_manager_notification_enabled = "isCaseManagerNotificationEnabled"
    is_additional_session_request_enabled = "isAdditionalSessionRequestEnabled"


class AccessCodeFilters(CamelModel):
    is_active: bool | None
    is_coach_session_enabled: bool | None
    is_communication_request_enabled: bool | None
    is_care_navigation_enabled: bool | None
    is_case_manager_notification_enabled: bool | None
    is_additional_session_request_enabled: bool | None


class AccessCodeSearchLookup(enum.Enum):
    name = "name"


class ClientSortQuery(enum.Enum):
    first_name = "firstName"
    last_name = "lastName"
    email = "email"
    is_active = "isActive"
    access_code = "accessCode"
    coach = "coach"


class ClientFilters(CamelModel):
    is_active: bool | None
    access_code: str | None
    coach: str | None


class ClientSearchLookup(enum.Enum):
    first_name = "firstName"
    last_name = "lastName"
    email = "email"


class CoachSortQuery(enum.Enum):
    first_name = "firstName"
    last_name = "lastName"
    email = "email"
    is_active = "isActive"


class CoachFilters(CamelModel):
    is_active: bool | None


class CoachSearchLookup(enum.Enum):
    first_name = "firstName"
    last_name = "lastName"
    email = "email"


class PaginationQuery(BaseModel):
    offset: int = Query(0, title="Starting point", ge=0)
    limit: int = Query(20, title="Records per request", ge=1, le=50)


class SortingQuery(BaseModel):
    sort: str | None = Query(None, title="Sorting field")
    sort_dir: Literal["asc", "desc"] = Query("asc", title="Sorting direction")


class PaginationResponse(BaseModel):
    offset: int
    limit: int
    total: int


class CoachesResponse(BaseModel):
    pagination: PaginationResponse
    coaches: list[Coach]


class ClientsResponse(BaseModel):
    pagination: PaginationResponse
    clients: list[Client]


class AccessCodesResponse(BaseModel):
    pagination: PaginationResponse
    codes: list[AccessCode]

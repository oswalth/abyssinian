from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from crud.base import SORT_TYPE, ASC
from crud.users import user_crud, coach_crud
from dependencies.db import get_db
from sqlalchemy.orm import Session

from schemas.query import PaginationQuery, CoachFilters, CoachSortQuery, CoachSearchLookup, CoachesResponse, \
    PaginationResponse
from schemas.users import CoachCreate, Coach

router = APIRouter(
    prefix="/coaches",
    tags=["coaches"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=CoachesResponse)
def read_coaches(
        pagination: PaginationQuery = Depends(),
        filters: CoachFilters = Depends(),
        search_value: str | None = Query(None, title="Search value", alias="q"),
        search_lookup: CoachSearchLookup = Query(CoachSearchLookup.first_name, title="Search lookup", alias="lookup"),
        sort: CoachSortQuery = Query(CoachSortQuery.first_name),
        sort_dir: SORT_TYPE = Query(ASC, alias="sortDir"),
        db: Session = Depends(get_db),
):
    coaches, total = coach_crud.get_many(
        db,
        sort=sort.name,
        sort_dir=sort_dir,
        filters=filters.dict(exclude_none=True),
        search_lookup=search_lookup.name,
        search_value=search_value,
        **pagination.dict()
    )
    return CoachesResponse(
        coaches=coaches,
        pagination=PaginationResponse(
            offset=pagination.offset,
            limit=pagination.limit,
            total=total
        )
    )


@router.get("/{coach_id}", response_model=Coach)
def read_coach(coach_id: UUID, db: Session = Depends(get_db)):
    db_coach = coach_crud.get(db, coach_id=coach_id)
    if db_coach is None:
        raise HTTPException(status_code=404, detail="Coach not found")
    return db_coach


@router.post("/", response_model=Coach)
def write_coach(coach: CoachCreate, db: Session = Depends(get_db)):
    db_coach = user_crud.get_user_by_email(db, email=coach.user.email)
    if db_coach:
        raise HTTPException(status_code=400, detail="Email already registered")
    return coach_crud.create(db=db, coach=coach)

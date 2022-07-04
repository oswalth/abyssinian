from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from crud.users import user_crud, coach_crud
from dependencies import get_db
from sqlalchemy.orm import Session

from schemas.users import CoachCreate, Coach

router = APIRouter(
    prefix="/coaches",
    tags=["coaches"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Coach])
def read_coaches(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coaches = coach_crud.get_many(db, offset=offset, limit=limit)
    return coaches


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

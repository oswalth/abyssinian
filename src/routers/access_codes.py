from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.users import access_code_crud
from dependencies import get_db
from schemas.users import AccessCode, AccessCodeCreate

router = APIRouter(
    prefix="/codes",
    tags=["codes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=AccessCode)
def write_access_code(access_code: AccessCodeCreate, db: Session = Depends(get_db)):
    db_code = access_code_crud.get_code_by_name(db, name=access_code.name)
    if db_code:
        raise HTTPException(status_code=400, detail="Access code already registered")
    return access_code_crud.create(db=db, obj_in=access_code)


@router.get("/", response_model=list[AccessCode])
def read_codes(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    access_codes = access_code_crud.get_many(db, offset=offset, limit=limit)
    return access_codes


@router.get("/{code_id}", response_model=list[AccessCode])
def read_code(code_id: UUID, db: Session = Depends(get_db)):
    db_code = access_code_crud.get(db, code_id=code_id)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Access code not found")
    return db_code

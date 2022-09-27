from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from crud.base import SORT_TYPE, DESC
from crud.users import access_code_crud
from dependencies.db import get_db
from schemas.query import AccessCodesResponse, PaginationResponse, PaginationQuery, AccessCodeFilters, \
    AccessCodeSearchLookup, AccessCodeSortQuery
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


@router.get("/", response_model=AccessCodesResponse)
def read_codes(
        pagination: PaginationQuery = Depends(),
        filters: AccessCodeFilters = Depends(),
        search_value: str | None = Query(None, title="Search value", alias="q"),
        search_lookup: AccessCodeSearchLookup = Query(AccessCodeSearchLookup.name, title="Search lookup", alias="lookup"),
        sort: AccessCodeSortQuery = Query(AccessCodeSortQuery.created_at),
        sort_dir: SORT_TYPE = Query(DESC, alias="sortDir"),
        db: Session = Depends(get_db),
):
    codes, total = access_code_crud.get_many(
        db,
        sort=sort.name,
        sort_dir=sort_dir,
        filters=filters.dict(exclude_none=True),
        search_lookup=search_lookup.name,
        search_value=search_value,
        **pagination.dict()
    )
    return AccessCodesResponse(
        codes=codes,
        pagination=PaginationResponse(
            offset=pagination.offset,
            limit=pagination.limit,
            total=total
        )
    )


@router.get("/{code_id}", response_model=list[AccessCode])
def read_code(code_id: UUID, db: Session = Depends(get_db)):
    db_code = access_code_crud.get(db, code_id=code_id)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Access code not found")
    return db_code

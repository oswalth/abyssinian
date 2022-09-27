from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body, Query

from crud.base import ASC, SORT_TYPE
from crud.users import user_crud, client_crud
from dependencies.db import get_db
from sqlalchemy.orm import Session

from schemas.query import PaginationQuery, ClientSortQuery, ClientFilters, ClientSearchLookup, ClientsResponse, \
    PaginationResponse
from schemas.users import ClientCreate, Client

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Client)
def write_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = user_crud.get_user_by_email(db, email=client.user.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return client_crud.create(db=db, client=client)


@router.get("/", response_model=ClientsResponse)
def read_clients(
        pagination: PaginationQuery = Depends(),
        filters: ClientFilters = Depends(),
        search_value: str | None = Query(None, title="Search value", alias="q"),
        search_lookup: ClientSearchLookup = Query(ClientSearchLookup.first_name, title="Search lookup", alias="lookup"),
        sort: ClientSortQuery = Query(ClientSortQuery.first_name),
        sort_dir: SORT_TYPE = Query(ASC, alias="sortDir"),
        db: Session = Depends(get_db),
):
    clients, total = client_crud.get_many(
        db,
        sort=sort.name,
        sort_dir=sort_dir,
        filters=filters.dict(exclude_none=True),
        search_lookup=search_lookup.name,
        search_value=search_value,
        **pagination.dict()
    )
    return ClientsResponse(
        clients=clients,
        pagination=PaginationResponse(
            offset=pagination.offset,
            limit=pagination.limit,
            total=total
        )
    )


@router.get("/{client_id}", response_model=Client)
def read_client(client_id: UUID, db: Session = Depends(get_db)):
    db_client = client_crud.get(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


@router.post("/{client_id}/set-coach", response_model=Client)
def set_coach(client_id: UUID, coach_id: UUID = Body(embed=True), db: Session = Depends(get_db)):
    return client_crud.set_client_coach(db, client_id=client_id, coach_id=coach_id)

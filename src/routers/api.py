from fastapi import APIRouter

from config import get_settings
from routers import access_codes, auth, clients, coaches


api_router = APIRouter(prefix=get_settings().api_str)
api_router.include_router(access_codes.router)
api_router.include_router(auth.router)
api_router.include_router(clients.router)
api_router.include_router(coaches.router)

from fastapi import APIRouter

from src.api.api_v1.endpoints import login, notes_authorized, notes_unauthorized, users

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    notes_unauthorized.router,
    prefix="/notes/unauthorized",
    tags=["notes"]
)
api_router.include_router(
    notes_authorized.router,
    prefix="/notes/authorized",
    tags=["notes"]
)

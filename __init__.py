
from fastapi import APIRouter

from .crud import db
from .views import scrum_generic_router
from .views_api import scrum_api_router

scrum_ext: APIRouter = APIRouter(prefix="/scrum", tags=["Scrum"])
scrum_ext.include_router(scrum_generic_router)
scrum_ext.include_router(scrum_api_router)


scrum_static_files = [
    {
        "path": "/scrum/static",
        "name": "scrum_static",
    }
]

__all__ = [
    "db",
    "scrum_ext",
    "scrum_static_files",
]

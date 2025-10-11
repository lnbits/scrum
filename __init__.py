import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_paid_invoices
from .views import scrum_generic_router
from .views_api import scrum_api_router

scrum_ext: APIRouter = APIRouter(
    prefix="/scrum", tags=["Scrum"]
)
scrum_ext.include_router(scrum_generic_router)
scrum_ext.include_router(scrum_api_router)


scrum_static_files = [
    {
        "path": "/scrum/static",
        "name": "scrum_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def scrum_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def scrum_start():
    task = create_permanent_unique_task("ext_scrum", wait_for_paid_invoices)
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "scrum_ext",
    "scrum_start",
    "scrum_static_files",
    "scrum_stop",
]
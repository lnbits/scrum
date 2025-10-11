# Description: This file contains the extensions API endpoints.
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.core.models import SimpleStatus, User
from lnbits.db import Filters, Page
from lnbits.decorators import (
    check_user_exists,
    parse_filters,
)
from lnbits.helpers import generate_filter_params_openapi

from .crud import (
    create_tasks,
    create_scrum,
    delete_tasks,
    delete_scrum,
    get_tasks_by_id,
    get_tasks_paginated,
    get_scrum,
    get_scrum_by_id,
    get_scrum_ids_by_user,
    get_scrum_paginated,
    update_tasks,
    update_scrum,
)
from .models import (
    Tasks,
    TasksFilters,
    CreateTasks,
    TasksPublic,
    CreateScrum,
    Scrum,
    ScrumFilters,
)
from loguru import logger

scrum_filters = parse_filters(ScrumFilters)
tasks_filters = parse_filters(TasksFilters)

scrum_api_router = APIRouter()


############################# Scrum #############################
@scrum_api_router.post("/api/v1/scrum", status_code=HTTPStatus.CREATED)
async def api_create_scrum(
    data: CreateScrum,
    user: User = Depends(check_user_exists),
) -> Scrum:
    scrum = await create_scrum(user.id, data)
    return scrum


@scrum_api_router.put("/api/v1/scrum/{scrum_id}", status_code=HTTPStatus.CREATED)
async def api_update_scrum(
    scrum_id: str,
    data: CreateScrum,
    user: User = Depends(check_user_exists),
) -> Scrum:
    scrum = await get_scrum(user.id, scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum not found.")
    if scrum.user_id != user.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this scrum.")
    scrum = await update_scrum(Scrum(**{**scrum.dict(), **data.dict()}))
    return scrum


@scrum_api_router.get(
    "/api/v1/scrum/paginated",
    name="Scrum List",
    summary="get paginated list of scrum",
    response_description="list of scrum",
    openapi_extra=generate_filter_params_openapi(ScrumFilters),
    response_model=Page[Scrum],
)
async def api_get_scrum_paginated(
    user: User = Depends(check_user_exists),
    filters: Filters = Depends(scrum_filters),
) -> Page[Scrum]:

    return await get_scrum_paginated(
        user_id=user.id,
        filters=filters,
    )


@scrum_api_router.get(
    "/api/v1/scrum/{scrum_id}",
    name="Get Scrum",
    summary="Get the scrum with this id.",
    response_description="An scrum or 404 if not found",
    response_model=Scrum,
)
async def api_get_scrum(
    scrum_id: str,
    user: User = Depends(check_user_exists),
) -> Scrum:

    scrum = await get_scrum(user.id, scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum not found.")

    return scrum


@scrum_api_router.delete(
    "/api/v1/scrum/{scrum_id}",
    name="Delete Scrum",
    summary="Delete the scrum " "and optionally all its associated tasks.",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_scrum(
    scrum_id: str,
    clear_tasks: bool | None = False,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    await delete_scrum(user.id, scrum_id)
    if clear_tasks is True:
        # await delete all tasks associated with this scrum
        pass
    return SimpleStatus(success=True, message="Scrum Deleted")


############################# Tasks #############################
@scrum_api_router.post(
    "/api/v1/tasks",
    name="Create Tasks",
    summary="Create new tasks for the specified scrum.",
    response_description="The created tasks.",
    response_model=Tasks,
    status_code=HTTPStatus.CREATED,
)
async def api_create_tasks(
    data: CreateTasks,
    user: User = Depends(check_user_exists),
) -> Tasks:
    scrum = await get_scrum(user.id, data.scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum not found.")

    tasks = await create_tasks(data)
    return tasks




@scrum_api_router.put(
    "/api/v1/tasks/{tasks_id}",
    name="Update Tasks",
    summary="Update the tasks with this id.",
    response_description="The updated tasks.",
    response_model=Tasks,
)
async def api_update_tasks(
    tasks_id: str,
    data: CreateTasks,
    user: User = Depends(check_user_exists),
) -> Tasks:
    tasks = await get_tasks_by_id(tasks_id)
    if not tasks:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Tasks not found.")

    scrum = await get_scrum(user.id, tasks.scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum not found.")

    tasks = await update_tasks(Tasks(**{**tasks.dict(), **data.dict()}))
    return tasks

@scrum_api_router.put(
    "/api/v1/tasks/public/{tasks_id}",
    name="Update Tasks",
    summary="Update the tasks with this id.",
    response_description="The updated tasks.",
    response_model=Tasks,
)
async def api_update_tasks(
    tasks_id: str,
    data: TasksPublic,
) -> Tasks:
    tasks = await get_tasks_by_id(tasks_id)
    if not tasks:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Task not found.")

    scrum = await get_scrum_by_id(tasks.scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum not found.")
    logger.debug(scrum.public_assigning)
    logger.debug(data.assignee )
    logger.debug(tasks.assignee)
    if (
        not scrum.public_assigning
        and data.assignee is not None
        and data.assignee != tasks.assignee
    ):
        raise HTTPException(HTTPStatus.FORBIDDEN, "You cant edit the assignee.")
    tasks = await update_tasks(Tasks(**{**tasks.dict(), **data.dict()}))
    return tasks

@scrum_api_router.get(
    "/api/v1/tasks/paginated",
    name="Tasks List",
    summary="get paginated list of tasks",
    response_description="list of tasks",
    openapi_extra=generate_filter_params_openapi(TasksFilters),
    response_model=Page[Tasks],
)
async def api_get_tasks_paginated(
    user: User = Depends(check_user_exists),
    scrum_id: str | None = None,
    filters: Filters = Depends(tasks_filters),
) -> Page[Tasks]:

    scrum_ids = await get_scrum_ids_by_user(user.id)

    if scrum_id:
        if scrum_id not in scrum_ids:
            raise HTTPException(HTTPStatus.FORBIDDEN, "Not your scrum.")
        scrum_ids = [scrum_id]

    return await get_tasks_paginated(
        scrum_ids=scrum_ids,
        filters=filters,
    )


@scrum_api_router.get(
    "/api/v1/tasks/{tasks_id}",
    name="Get Tasks",
    summary="Get the tasks with this id.",
    response_description="An tasks or 404 if not found",
    response_model=Tasks,
)
async def api_get_tasks(
    tasks_id: str,
    user: User = Depends(check_user_exists),
) -> Tasks:

    tasks = await get_tasks_by_id(tasks_id)
    if not tasks:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Tasks not found.")
    scrum = await get_scrum(user.id, tasks.scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum deleted for this Tasks.")

    return tasks


@scrum_api_router.delete(
    "/api/v1/tasks/{tasks_id}",
    name="Delete Tasks",
    summary="Delete the tasks",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_tasks(
    tasks_id: str,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    tasks = await get_tasks_by_id(tasks_id)
    if not tasks:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Tasks not found.")
    scrum = await get_scrum(user.id, tasks.scrum_id)
    if not scrum:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Scrum deleted for this Tasks.")

    await delete_tasks(scrum.id, tasks_id)
    return SimpleStatus(success=True, message="Tasks Deleted")



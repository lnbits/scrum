# Description: This file contains the CRUD operations for talking to the database.


from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    Tasks,
    TasksFilters,
    CreateTasks,
    CreateScrum,
    Scrum,
    ScrumFilters,
)

db = Database("ext_scrum")


########################### Scrum ############################
async def create_scrum(user_id: str, data: CreateScrum) -> Scrum:
    scrum = Scrum(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("scrum.scrum", scrum)
    return scrum


async def get_scrum(
    user_id: str,
    scrum_id: str,
) -> Scrum | None:
    return await db.fetchone(
        """
            SELECT * FROM scrum.scrum
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": scrum_id, "user_id": user_id},
        Scrum,
    )


async def get_scrum_by_id(
    scrum_id: str,
) -> Scrum | None:
    return await db.fetchone(
        """
            SELECT * FROM scrum.scrum
            WHERE id = :id
        """,
        {"id": scrum_id},
        Scrum,
    )


async def get_scrum_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM scrum.scrum
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


async def get_scrum_paginated(
    user_id: str | None = None,
    filters: Filters[ScrumFilters] | None = None,
) -> Page[Scrum]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM scrum.scrum",
        where=where,
        values=values,
        filters=filters,
        model=Scrum,
    )


async def update_scrum(data: Scrum) -> Scrum:
    await db.update("scrum.scrum", data)
    return data


async def delete_scrum(user_id: str, scrum_id: str) -> None:
    await db.execute(
        """
            DELETE FROM scrum.scrum
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": scrum_id, "user_id": user_id},
    )


################################# Tasks ###########################


async def create_tasks(scrum_id: str, data: CreateTasks) -> Tasks:
    tasks = Tasks(**data.dict(), id=urlsafe_short_hash(), scrum_id=scrum_id)
    await db.insert("scrum.tasks", tasks)
    return tasks


async def get_tasks(
    scrum_id: str,
    tasks_id: str,
) -> Tasks | None:
    return await db.fetchone(
        """
            SELECT * FROM scrum.tasks
            WHERE id = :id AND scrum_id = :scrum_id
        """,
        {"id": tasks_id, "scrum_id": scrum_id},
        Tasks,
    )


async def get_tasks_by_id(
    tasks_id: str,
) -> Tasks | None:
    return await db.fetchone(
        """
            SELECT * FROM scrum.tasks
            WHERE id = :id
        """,
        {"id": tasks_id},
        Tasks,
    )


async def get_tasks_paginated(
    scrum_ids: list[str] | None = None,
    filters: Filters[TasksFilters] | None = None,
) -> Page[Tasks]:

    if not scrum_ids:
        return Page(data=[], total=0)

    where = []
    values = {}
    id_clause = []
    for i, item_id in enumerate(scrum_ids):
        # scrum_ids are not user input, but DB entries, so this is safe
        scrum_id = f"scrum_id__{i}"
        id_clause.append(f"scrum_id = :{scrum_id}")
        values[scrum_id] = item_id
    or_clause = " OR ".join(id_clause)
    where.append(f"({or_clause})")

    return await db.fetch_page(
        "SELECT * FROM scrum.tasks",
        where=where,
        values=values,
        filters=filters,
        model=Tasks,
    )


async def update_tasks(data: Tasks) -> Tasks:
    await db.update("scrum.tasks", data)
    return data


async def delete_tasks(scrum_id: str, tasks_id: str) -> None:
    await db.execute(
        """
            DELETE FROM scrum.tasks
            WHERE id = :id AND scrum_id = :scrum_id
        """,
        {"id": tasks_id, "scrum_id": scrum_id},
    )



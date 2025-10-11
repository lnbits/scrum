from datetime import datetime, timezone
from enum import Enum

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


class TaskStage(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


########################### Scrum ############################
class CreateScrum(BaseModel):
    name: str
    description: str
    public_assigning: bool
    wallet: str


class Scrum(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    public_assigning: bool
    wallet: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ScrumFilters(FilterModel):
    __search_fields__ = [
        "name",
        "description",
        "public_assigning",
    ]

    __sort_fields__ = [
        "name",
        "description",
        "public_assigning",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


################################# Tasks ###########################


class CreateTasks(BaseModel):
    task: str
    scrum_id: str
    assignee: str | None
    stage: TaskStage = TaskStage.todo
    reward: int | None
    complete: bool | None
    notes: str | None


class TasksPublic(BaseModel):
    assignee: str | None
    stage: TaskStage = TaskStage.todo
    notes: str | None


class Tasks(BaseModel):
    id: str
    task: str
    scrum_id: str
    assignee: str | None
    stage: TaskStage
    reward: int | None
    paid: bool = False
    complete: bool = False
    notes: str | None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TasksFilters(FilterModel):
    __search_fields__ = [
        "scrum",
        "task",
        "assignee",
        "stage",
        "reward",
        "complete",
        "notes",
    ]

    __sort_fields__ = [
        "scrum",
        "task",
        "assignee",
        "stage",
        "reward",
        "complete",
        "notes",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None

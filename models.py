from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


########################### Scrum ############################
class CreateScrum(BaseModel):
    name: str | None
    description: str
    progress: int | None
    


class Scrum(BaseModel):
    id: str
    user_id: str
    name: str | None
    description: str
    progress: int | None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ScrumFilters(FilterModel):
    __search_fields__ = [
        "name","description","progress",
    ]

    __sort_fields__ = [
        "name",
        "description",
        "progress",
        
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


################################# Tasks ###########################


class CreateTasks(BaseModel):
    scrum: bool
    task: str
    assignee: str | None
    stage: str
    progress: int | None
    reward: int | None
    complete: bool | None
    notes: str | None
    


class Tasks(BaseModel):
    id: str
    scrum_id: str
    scrum: bool
    task: str
    assignee: str | None
    stage: str
    progress: int | None
    reward: int | None
    complete: bool | None
    notes: str | None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))




class TasksFilters(FilterModel):
    __search_fields__ = [
        "scrum","task","assignee","stage","progress","reward","complete","notes",
    ]

    __sort_fields__ = [
        "scrum",
        "task",
        "assignee",
        "stage",
        "progress",
        "reward",
        "complete",
        "notes",
        
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None



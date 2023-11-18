__all__ = ["ViewTask", "ViewTaskComment", "ChangeTaskStatus", "FlatViewTask", "FlatViewTaskType"]

import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.modules.users.schemas import ViewUser
from src.storages.sqlalchemy.models.tasks import TaskStatuses


class FlatViewTaskType(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None


class FlatViewTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # exclude relations
    id: int
    type: FlatViewTaskType
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatuses] = None
    priority: Optional[str] = None
    location: Optional[str] = None

    starting: Optional[datetime.datetime] = None
    deadline: Optional[datetime.datetime] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    current_machine: Optional["FlatViewMachine"] = None


class ViewTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # TODO:
    type: FlatViewTaskType
    title: Optional[str] = None
    description: Optional[str] = None
    asignee: Optional[ViewUser] = None
    status: Optional[TaskStatuses] = None
    priority: Optional[str] = None
    location: Optional[str] = None

    starting: Optional[datetime.datetime] = None
    deadline: Optional[datetime.datetime] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    # TODO: Something with this
    # work_volume: Optional[float] = None
    # payment_coefficient: Optional[float] = None
    # fuel_consumption: Optional[float] = None
    # agregate_depth: Optional[float] = None
    # agregate_working_speed: Optional[float] = None
    # agregate_solvent_consumption: Optional[float] = None

    current_machine: Optional["FlatViewMachine"] = None

    current_agregate: Optional["FlatViewAgregate"] = None

    # TODO: TaskComment schemas
    # comments: Optional[list["ViewTaskComment"]] = None  # ????
    # TODO: TaskStatusHistory schemas
    # status_history: Optional[list["TaskStatusHistory"]] = None


class ViewTaskComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    task_id: int
    user_id: int

    task: ViewTask
    user: ViewUser

    text: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ChangeTaskStatus(BaseModel):
    status: TaskStatuses


from src.modules.machines.schemas import FlatViewMachine  # noqa: E402

# noinspection PyUnresolvedReferences
from src.modules.agregates.schemas import FlatViewAgregate  # noqa: E402, F401

ViewTask.model_rebuild()

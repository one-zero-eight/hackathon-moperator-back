__all__ = ["ViewTask", "ViewTaskComment"]

import datetime
from typing import Optional
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from src.modules.users.schemas import ViewUser


class TaskStatuses(StrEnum):
    first_status = "fs"
    second_status = "ss"
    third_status = "ts"


class ViewTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    asignee_id: Optional[int] = None
    asignee: Optional[ViewUser] = None
    status: Optional[TaskStatuses] = None
    priority: Optional[str] = None
    location: Optional[str] = None

    starting: Optional[datetime.datetime] = None
    deadline: Optional[datetime.datetime] = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    work_volume: Optional[float] = None
    payment_coefficient: Optional[float] = None

    fuel_consumption: Optional[float] = None

    agregate_depth: Optional[float] = None
    agregate_working_speed: Optional[float] = None
    agregate_solvent_consumption: Optional[float] = None

    # TODO: Machine schemas
    suitable_machines: Optional[list["ViewMachine"]] = None
    current_machine_id: Optional[int] = None
    current_machine: Optional["ViewMachine"] = None

    # TODO: Agregate schemas
    suitable_agregates: Optional[list["ViewAgregate"]] = None
    current_agregate_id: Optional[int] = None
    current_agregate: Optional["ViewAgregate"] = None

    comments: Optional[list["ViewTaskComment"]] = None  # ????

    status_history: Optional[list["TaskStatusHistory"]] = None


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


ViewTask.model_rebuild()

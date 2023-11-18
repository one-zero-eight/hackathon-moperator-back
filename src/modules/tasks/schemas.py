__all__ = ["ViewTask", "ViewTaskComment"]

import datetime
from typing import Optional
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from src.modules.users.schemas import ViewUser
from src.storages.sqlalchemy.models.tasks import TaskStatuses


class ViewTask(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "type": "type",
                "title": "title",
                "description": "description",
                "asignee_id": 1,
                "asignee": {
                    "id": 1,
                    "name": "name",
                    "surname": "surname",
                    "email": "email",
                    "phone": "phone",
                    "role": "role",
                    "status": "status",
                    "created_at": "2021-10-07T16:41:32.000000",
                    "updated_at": "2021-10-07T16:41:32.000000",
                },
                "status": "fs",
                "priority": "priority",
                "location": "location",
                "starting": "2021-10-07T16:41:32.000000",
                "deadline": "2021-10-07T16:41:32.000000",
                "created_at": "2021-10-07T16:41:32.000000",
                "updated_at": "2021-10-07T16:41:32.000000",
                "work_volume": 1.0,
                "payment_coefficient": 1.0,
                "fuel_consumption": 1.0,
                "agregate_depth": 1.0,
                "agregate_working_speed": 1.0,
                "agregate_solvent_consumption": 1.0,
                "comments": [
                    {
                        "id": 1,
                        "task_id": 1,
                        "user_id": 1,
                        "task": {
                            "id": 1,
                            "type": "type",
                            "title": "title",
                            "description": "description",
                            "asignee_id": 1,
                            "asignee": {
                                "id": 1,
                                "name": "name",
                                "surname": "surname",
                                "email": "email",
                                "phone": "phone",
                                "role": "role",
                                "status": "status",
                                "created_at": "2021-10-07T16:41:32.000000",
                                "updated_at": "2021-10-07T16:41:32.000000",
                            },
                            "status": "fs",
                            "priority": "priority",
                            "location": "location",
                            "starting": "2021-10-07T16:41:32.000000",
                            "deadline": "2021-10-07T16:41:32.000000",
                            "created_at": "2021-10-07T16:41:32.000000",
                            "updated_at": "2021-10-07T16:41:32.000000",
                            "work_volume": 1.0,
                            "payment_coefficient": 1.0,
                            "fuel_consumption": 1.0,
                            "agregate_depth": 1.0,
                            "agregate_working_speed": 1.0,
                            "agregate_solvent_consumption": 1.0,
                        },
                    }
                ],
            }
        },
    )

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
    # suitable_machines: Optional[list["ViewMachine"]] = None
    # current_machine_id: Optional[int] = None
    # current_machine: Optional["ViewMachine"] = None

    # TODO: Agregate schemas
    # suitable_agregates: Optional[list["ViewAgregate"]] = None
    # current_agregate_id: Optional[int] = None
    # current_agregate: Optional["ViewAgregate"] = None

    comments: Optional[list["ViewTaskComment"]] = None  # ????
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


ViewTask.model_rebuild()

__all__ = ["ViewMachine", "FlatViewMachine"]

from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.storages.sqlalchemy.models.machines import MachineStatus


class FlatViewMachine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    status: MachineStatus
    current_location: Optional[str] = None


class ViewMachine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    description: Optional[str] = None
    status: MachineStatus
    current_location: Optional[str] = None

    suitable_tasks: Optional[list["FlatViewTask"]] = None
    current_task: Optional["FlatViewTask"] = None

    suitable_agregates: Optional[list["FlatViewAgregate"]] = None


from src.modules.tasks.schemas import FlatViewTask  # noqa: E402
from src.modules.agregates.schemas import FlatViewAgregate  # noqa: E402

ViewMachine.model_rebuild()

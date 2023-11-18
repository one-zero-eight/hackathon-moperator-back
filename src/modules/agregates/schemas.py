__all__ = ["ViewAgregate", "FlatViewAgregate"]

from typing import Optional

from pydantic import BaseModel, ConfigDict


class FlatViewAgregate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    status: str
    current_location: Optional[str] = None


class ViewAgregate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    description: Optional[str] = None
    status: str
    current_location: Optional[str] = None

    suitable_tasks: Optional[list["FlatViewTask"]] = None
    current_task: Optional["FlatViewTask"] = None

    suitable_machines: Optional[list["FlatViewMachine"]] = None


from src.modules.tasks.schemas import FlatViewTask  # noqa: E402
from src.modules.machines.schemas import FlatViewMachine  # noqa: E402

ViewAgregate.model_rebuild()

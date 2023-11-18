__all__ = ["ViewAgregate"]

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ViewAgregate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    description: Optional[str] = None
    status: str
    current_location: Optional[str] = None

    suitable_tasks: Optional[list["ViewTask"]] = None
    current_task: Optional["ViewTask"] = None

    suitable_machines: Optional[list["ViewMachine"]] = None


from src.modules.tasks.schemas import ViewTask  # noqa: E402
from src.modules.machines.schemas import ViewMachine  # noqa: E402

ViewAgregate.model_rebuild()

__all__ = ["ViewMachine"]

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ViewMachine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    type: str
    description: Optional[str] = None
    status: str
    current_location: Optional[str] = None

    suitable_tasks: Optional[list["ViewTask"]] = None
    current_task: Optional["ViewTask"] = None

    suitable_agregates: Optional[list["ViewAgregate"]] = None


from src.modules.agregates.schema import ViewAgregate  # noqa: E402
from src.modules.tasks.schemas import ViewTask  # noqa: E402

ViewMachine.model_rebuild()

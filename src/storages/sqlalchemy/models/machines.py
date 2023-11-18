__all__ = ["Machine", "MachineStatus"]

from enum import StrEnum

from src.storages.sqlalchemy.utils import *
from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.tasks import Task, TaskType
    from src.storages.sqlalchemy.models.agregates import Agregate


class MachineStatus(StrEnum):
    free = "free"
    busy = "busy"
    broken = "broken"


class Machine(Base, IdMixin):
    __tablename__ = "machines"

    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    # noinspection PyTypeChecker
    status: Mapped[MachineStatus] = mapped_column(
        SQLEnum(MachineStatus), nullable=False, server_default=MachineStatus.free.value
    )
    current_location: Mapped[Optional[str]] = mapped_column(nullable=True)

    suitable_task_types: Mapped[Optional[list["TaskType"]]] = relationship(
        "TaskType", secondary="task_suitable_machines"
    )

    current_task: Mapped[Optional["Task"]] = relationship("Task", back_populates="current_machine")
    suitable_agregates: Mapped[Optional[list["Agregate"]]] = relationship(
        "Agregate", secondary="agregate_suitable_machines", back_populates="suitable_machines"
    )

    def __repr__(self):
        return f"{self.name}"

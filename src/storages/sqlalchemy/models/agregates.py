__all__ = ["Agregate", "AgregateSuitableMachines"]

from enum import StrEnum

from src.storages.sqlalchemy.utils import *
from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.tasks import Task, TaskType
    from src.storages.sqlalchemy.models.machines import Machine


class AgregateStatus(StrEnum):
    free = "free"
    busy = "busy"
    broken = "broken"


class Agregate(Base, IdMixin):
    __tablename__ = "agregates"

    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    # noinspection PyTypeChecker
    status: Mapped[AgregateStatus] = mapped_column(
        SQLEnum(AgregateStatus), nullable=False, server_default=AgregateStatus.free.value
    )
    current_location: Mapped[Optional[str]] = mapped_column(nullable=True)

    suitable_task_types: Mapped[Optional[list["TaskType"]]] = relationship(
        "TaskType", secondary="task_suitable_agregates", back_populates="suitable_agregates", lazy="selectin"
    )
    tasks: Mapped[Optional[list["Task"]]] = relationship("Task", lazy="selectin")

    suitable_machines: Mapped[Optional[list["Machine"]]] = relationship(
        "Machine", secondary="agregate_suitable_machines", back_populates="suitable_agregates", lazy="selectin"
    )

    def __repr__(self):
        return f"{self.name} ({self.status})"


class AgregateSuitableMachines(Base):
    __tablename__ = "agregate_suitable_machines"

    agregate_id: Mapped[int] = mapped_column(ForeignKey(Agregate.id), primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), primary_key=True)

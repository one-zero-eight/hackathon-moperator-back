__all__ = ["Machine", "MachineStatus"]

from enum import StrEnum

from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, TEXT

from src.storages.sqlalchemy.utils import *
from src.storages.sqlalchemy.models.__mixin__ import IdMixin, NoneFileType
from src.storages.sqlalchemy.models.base import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.tasks import Task, TaskType
    from src.storages.sqlalchemy.models.agregates import Agregate


machines_attachments_storage = FileSystemStorage(path="./tmp")


class MachineStatus(StrEnum):
    free = "free"
    busy = "busy"
    broken = "broken"


class Machine(Base, IdMixin):
    __tablename__ = "machines"

    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(TEXT(), default="")
    # noinspection PyTypeChecker
    status: Mapped[MachineStatus] = mapped_column(
        SQLEnum(MachineStatus), nullable=False, server_default=MachineStatus.free.value
    )
    current_location: Mapped[Optional[str]] = mapped_column(nullable=True)

    suitable_task_types: Mapped[Optional[list["TaskType"]]] = relationship(
        "TaskType", secondary="task_suitable_machines", lazy="selectin"
    )

    tasks: Mapped[Optional[list["Task"]]] = relationship("Task", lazy="selectin")

    suitable_agregates: Mapped[Optional[list["Agregate"]]] = relationship(
        "Agregate", secondary="agregate_suitable_machines", back_populates="suitable_machines", lazy="selectin"
    )

    attachments = Column(NoneFileType(storage=machines_attachments_storage), nullable=True)

    def __repr__(self):
        return f"{self.name} ({self.status})"

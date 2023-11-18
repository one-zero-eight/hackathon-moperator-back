__all__ = ["Machine"]

from src.storages.sqlalchemy.utils import *
from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.tasks import Task
    from src.storages.sqlalchemy.models.agregates import Agregate


class Machine(Base, IdMixin):
    __tablename__ = "machines"

    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False, default="free")
    current_location: Mapped[Optional[str]] = mapped_column(nullable=True)

    suitable_tasks: Mapped[Optional[list["Task"]]] = relationship("Task", secondary="task_suitable_machines")
    current_task: Mapped[Optional["Task"]] = relationship(
        "Task",
        primaryjoin="and_(Task.current_machine_id==Machine.id, Task.status=='in_progress')",
    )

    suitable_agregates: Mapped[Optional[list["Agregate"]]] = relationship(
        "Agregate", secondary="agregate_suitable_machines", back_populates="suitable_machines"
    )

    def __repr__(self):
        return f"Machine({self.name}: {self.type})"

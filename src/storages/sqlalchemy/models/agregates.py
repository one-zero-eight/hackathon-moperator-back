__all__ = ["Agregate", "AgregateSuitableMachines"]

from src.storages.sqlalchemy.utils import *
from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.tasks import Task
    from src.storages.sqlalchemy.models.machines import Machine


class Agregate(Base, IdMixin):
    __tablename__ = "agregates"

    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False, default="free")
    current_location: Mapped[Optional[str]] = mapped_column(nullable=True)

    suitable_tasks: Mapped[Optional[list["Task"]]] = relationship(
        "Task", secondary="task_suitable_agregates", back_populates="suitable_agregates"
    )
    current_task: Mapped[Optional["Task"]] = relationship("Task")

    suitable_machines: Mapped[Optional[list["Machine"]]] = relationship(
        "Machine", secondary="agregate_suitable_machines", back_populates="suitable_agregates"
    )

    def __repr__(self):
        return f"Agregate({self.name}: {self.type})"


class AgregateSuitableMachines(Base):
    __tablename__ = "agregate_suitable_machines"

    agregate_id: Mapped[int] = mapped_column(ForeignKey(Agregate.id), primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), primary_key=True)

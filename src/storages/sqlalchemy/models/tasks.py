__all__ = [
    "Task",
    "TaskSuitableMachines",
    "TaskComment",
    "TaskStatusHistory",
    "TaskSuitableAgregates",
]

import datetime

from src.storages.sqlalchemy.utils import *
from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.users import User
    from src.storages.sqlalchemy.models.machines import Machine
    from src.storages.sqlalchemy.models.agregates import Agregate


class Task(Base, IdMixin):
    __tablename__ = "tasks"

    type: Mapped[Optional[str]] = mapped_column(nullable=False, default="task")
    title: Mapped[Optional[str]] = mapped_column(nullable=False, default="Task title")
    description: Mapped[Optional[str]] = mapped_column(default="")
    asignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user_data.user_id"), nullable=True)
    asignee: Mapped[Optional["User"]] = relationship()
    status: Mapped[Optional[str]] = mapped_column(nullable=False, default="draft")
    priority: Mapped[Optional[str]] = mapped_column(nullable=False, default="low")
    location: Mapped[Optional[str]] = mapped_column(nullable=False, default="")

    starting: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    deadline: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    work_volume: Mapped[Optional[float]] = mapped_column(nullable=True)
    payment_coefficient: Mapped[Optional[float]] = mapped_column(nullable=True)

    fuel_consumption: Mapped[Optional[float]] = mapped_column(nullable=True)

    agregate_depth: Mapped[Optional[float]] = mapped_column(nullable=True)
    agregate_working_speed: Mapped[Optional[float]] = mapped_column(nullable=True)
    agregate_solvent_consumption: Mapped[Optional[float]] = mapped_column(nullable=True)

    suitable_machines: Mapped[Optional[list["Machine"]]] = relationship(
        "Machine", secondary="task_suitable_machines", back_populates="suitable_tasks"
    )
    current_machine_id: Mapped[Optional[int]] = mapped_column(ForeignKey("machines.id"), nullable=True)
    current_machine: Mapped[Optional["Machine"]] = relationship("Machine", back_populates="current_task")

    suitable_agregates: Mapped[Optional[list["Agregate"]]] = relationship(
        "Agregate", secondary="task_suitable_agregates", back_populates="suitable_tasks"
    )
    current_agregate_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agregates.id"), nullable=True)
    current_agregate: Mapped[Optional["Agregate"]] = relationship("Agregate", back_populates="current_task")

    comments: Mapped[Optional[list["TaskComment"]]] = relationship("TaskComment", back_populates="task")

    status_history: Mapped[Optional[list["TaskStatusHistory"]]] = relationship(
        "TaskStatusHistory", back_populates="task"
    )

    def __repr__(self):
        return f"Task({self.title})"


class TaskSuitableMachines(Base):
    __tablename__ = "task_suitable_machines"

    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id), primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), primary_key=True)


class TaskSuitableAgregates(Base):
    __tablename__ = "task_suitable_agregates"

    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id), primary_key=True)
    agregate_id: Mapped[int] = mapped_column(ForeignKey("agregates.id"), primary_key=True)


class TaskComment(Base, IdMixin):
    __tablename__ = "task_comments"

    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.user_id"), nullable=False)

    task: Mapped[Task] = relationship(Task)
    user: Mapped["User"] = relationship("User")

    text: Mapped[Optional[str]] = mapped_column(nullable=False, default="")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )


class TaskStatusHistory(Base, IdMixin):
    __tablename__ = "task_status_history"

    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.user_id"), primary_key=True)

    task: Mapped[Task] = relationship(Task)
    user: Mapped["User"] = relationship("User")

    status: Mapped[Optional[str]] = mapped_column(nullable=False)

    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

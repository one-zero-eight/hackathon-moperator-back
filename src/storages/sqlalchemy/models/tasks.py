__all__ = [
    "Task",
    "TaskType",
    "TaskSuitableMachines",
    "TaskComment",
    "TaskStatusHistory",
    "TaskSuitableAgregates",
    "TaskStatuses",
    "TaskPriority",
]

import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.utils import *

if TYPE_CHECKING:
    from src.storages.sqlalchemy.models.users import User
    from src.storages.sqlalchemy.models.machines import Machine
    from src.storages.sqlalchemy.models.agregates import Agregate


class TaskStatuses(StrEnum):
    draft = "draft"
    assigned = "assigned"
    in_progress = "in_progress"
    paused = "paused"
    completed = "completed"
    canceled = "canceled"


class TaskPriority(StrEnum):
    undefined = "undefined"
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base, IdMixin):
    __tablename__ = "tasks"

    title: Mapped[Optional[str]] = mapped_column(nullable=False, default="Task title #1")

    type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("task_types.id"), nullable=False)
    type: Mapped[Optional["TaskType"]] = relationship("TaskType", lazy="joined")

    asignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user_data.user_id"), nullable=True)
    asignee: Mapped[Optional["User"]] = relationship(lazy="joined")

    # noinspection PyTypeChecker
    status: Mapped[TaskStatuses] = mapped_column(
        SQLEnum(TaskStatuses), nullable=False, server_default=TaskStatuses.draft.value
    )

    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority), nullable=False, default=TaskPriority.undefined
    )
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

    current_machine_id: Mapped[Optional[int]] = mapped_column(ForeignKey("machines.id"), nullable=True)
    current_machine: Mapped[Optional["Machine"]] = relationship("Machine", back_populates="current_task", lazy="joined")
    current_agregate_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agregates.id"), nullable=True)
    current_agregate: Mapped[Optional["Agregate"]] = relationship(
        "Agregate", back_populates="current_task", lazy="joined"
    )

    comments: Mapped[Optional[list["TaskComment"]]] = relationship(
        "TaskComment", back_populates="task", order_by="desc(TaskComment.created_at)", lazy="selectin"
    )

    status_history: Mapped[Optional[list["TaskStatusHistory"]]] = relationship(
        "TaskStatusHistory", back_populates="task", order_by="desc(TaskStatusHistory.timestamp)", lazy="selectin"
    )

    def __repr__(self):
        return f"{self.title}"


class TaskType(Base, IdMixin):
    __tablename__ = "task_types"

    title: Mapped[Optional[str]] = mapped_column(nullable=False, default="Task title")
    description: Mapped[Optional[str]] = mapped_column(default="")
    suitable_machines: Mapped[Optional[list["Machine"]]] = relationship(
        "Machine", secondary="task_suitable_machines", back_populates="suitable_task_types"
    )
    suitable_agregates: Mapped[Optional[list["Agregate"]]] = relationship(
        "Agregate", secondary="task_suitable_agregates", back_populates="suitable_task_types"
    )

    tasks: Mapped[Optional[list[Task]]] = relationship("Task", back_populates="type")

    def __repr__(self):
        return f"{self.title}"


class TaskSuitableMachines(Base):
    __tablename__ = "task_suitable_machines"

    task_type_id: Mapped[int] = mapped_column(ForeignKey(TaskType.id), primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), primary_key=True)


class TaskSuitableAgregates(Base):
    __tablename__ = "task_suitable_agregates"

    task_type_id: Mapped[int] = mapped_column(ForeignKey(TaskType.id), primary_key=True)
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

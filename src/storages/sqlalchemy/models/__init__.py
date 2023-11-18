from src.storages.sqlalchemy.models.base import Base
import src.storages.sqlalchemy.models.__mixin__  # noqa: F401

# Add all models here
from src.storages.sqlalchemy.models.users import User, EmailFlow, UserRoles
from src.storages.sqlalchemy.models.machines import Machine
from src.storages.sqlalchemy.models.tasks import (
    Task,
    TaskSuitableMachines,
    TaskComment,
    TaskStatusHistory,
    TaskSuitableAgregates,
)
from src.storages.sqlalchemy.models.agregates import Agregate, AgregateSuitableMachines

__all__ = [
    "Base",
    "User",
    "EmailFlow",
    "UserRoles",
    "Machine",
    "Task",
    "TaskSuitableMachines",
    "TaskComment",
    "TaskStatusHistory",
    "TaskSuitableAgregates",
    "Agregate",
    "AgregateSuitableMachines",
]

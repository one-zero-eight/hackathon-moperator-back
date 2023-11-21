__all__ = [
    "DEPENDS",
    "DEPENDS_STORAGE",
    "DEPENDS_USER_REPOSITORY",
    "DEPENDS_VERIFIED_REQUEST",
    "DEPENDS_AUTH_REPOSITORY",
    "DEPENDS_TASK_REPOSITORY",
    "DEPENDS_MACHINE_REPOSITORY",
    "DEPENDS_AGREGATE_REPOSITORY",
    "Dependencies",
]

from fastapi import Depends

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.agregates.repository import AgregateRepository
    from src.modules.machines.repository import MachineRepository
    from src.modules.users.repository import UserRepository
    from src.modules.auth.repository import AuthRepository
    from src.modules.tasks.repository import TaskRepository
    from src.storages.sqlalchemy.storage import SQLAlchemyStorage


class Dependencies:
    _storage: "SQLAlchemyStorage"
    _user_repository: "UserRepository"
    _auth_repository: "AuthRepository"
    _task_repository: "TaskRepository"
    _machine_repository: "MachineRepository"
    _agregate_repository: "AgregateRepository"

    @classmethod
    def get_storage(cls) -> "SQLAlchemyStorage":
        return cls._storage

    @classmethod
    def set_storage(cls, storage: "SQLAlchemyStorage"):
        cls._storage = storage

    @classmethod
    def get_user_repository(cls) -> "UserRepository":
        return cls._user_repository

    @classmethod
    def set_user_repository(cls, user_repository: "UserRepository"):
        cls._user_repository = user_repository

    @classmethod
    def get_auth_repository(cls) -> "AuthRepository":
        return cls._auth_repository

    @classmethod
    def set_auth_repository(cls, auth_repository: "AuthRepository"):
        cls._auth_repository = auth_repository

    @classmethod
    def get_task_repository(cls) -> "TaskRepository":
        return cls._task_repository

    @classmethod
    def set_task_repository(cls, task_repository: "TaskRepository"):
        cls._task_repository = task_repository

    @classmethod
    def get_machine_repository(cls) -> "MachineRepository":
        return cls._machine_repository

    @classmethod
    def set_machine_repository(cls, machine_repository: "MachineRepository"):
        cls._machine_repository = machine_repository

    @classmethod
    def get_agregate_repository(cls) -> "AgregateRepository":
        return cls._agregate_repository

    @classmethod
    def set_agregate_repository(cls, agregate_repository: "AgregateRepository"):
        cls._agregate_repository = agregate_repository


DEPENDS = Depends(lambda: Dependencies)
"""It's a dependency injection container for FastAPI.
See `FastAPI docs <(https://fastapi.tiangolo.com/tutorial/dependencies/)>`_ for more info"""
DEPENDS_STORAGE = Depends(Dependencies.get_storage)
DEPENDS_USER_REPOSITORY = Depends(Dependencies.get_user_repository)
DEPENDS_AUTH_REPOSITORY = Depends(Dependencies.get_auth_repository)
DEPENDS_TASK_REPOSITORY = Depends(Dependencies.get_task_repository)
DEPENDS_MACHINE_REPOSITORY = Depends(Dependencies.get_machine_repository)
DEPENDS_AGREGATE_REPOSITORY = Depends(Dependencies.get_agregate_repository)

from src.modules.auth.dependencies import verify_request  # noqa: E402

DEPENDS_VERIFIED_REQUEST = Depends(verify_request)

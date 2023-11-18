__all__ = [
    "DEPENDS",
    "DEPENDS_SMTP_REPOSITORY",
    "DEPENDS_STORAGE",
    "DEPENDS_USER_REPOSITORY",
    "DEPENDS_VERIFIED_REQUEST",
    "DEPENDS_AUTH_REPOSITORY",
    "DEPENDS_TASK_REPOSITORY",
    "DEPENDS_MACHINE_REPOSITORY",
    "Dependencies",
]

from fastapi import Depends

from src.modules.agregates.abc import AbstractAgregateRepository
from src.modules.machines.abc import AbstractMachineRepository
from src.modules.smtp.abc import AbstractSMTPRepository
from src.modules.users.abc import AbstractUserRepository
from src.modules.auth.abc import AbstractAuthRepository
from src.modules.tasks.abc import AbstractTaskRepository
from src.storages.sqlalchemy.storage import AbstractSQLAlchemyStorage


class Dependencies:
    _storage: "AbstractSQLAlchemyStorage"
    _user_repository: "AbstractUserRepository"
    _smtp_repository: "AbstractSMTPRepository"
    _auth_repository: "AbstractAuthRepository"
    _task_repository: "AbstractTaskRepository"
    _machine_repository: "AbstractMachineRepository"
    _agregate_repository: "AbstractAgregateRepository"

    @classmethod
    def get_storage(cls) -> "AbstractSQLAlchemyStorage":
        return cls._storage

    @classmethod
    def set_storage(cls, storage: "AbstractSQLAlchemyStorage"):
        cls._storage = storage

    @classmethod
    def get_user_repository(cls) -> "AbstractUserRepository":
        return cls._user_repository

    @classmethod
    def set_user_repository(cls, user_repository: "AbstractUserRepository"):
        cls._user_repository = user_repository

    @classmethod
    def get_smtp_repository(cls) -> "AbstractSMTPRepository":
        return cls._smtp_repository

    @classmethod
    def set_smtp_repository(cls, smtp_repository: "AbstractSMTPRepository"):
        cls._smtp_repository = smtp_repository

    @classmethod
    def get_auth_repository(cls) -> "AbstractAuthRepository":
        return cls._auth_repository

    @classmethod
    def set_auth_repository(cls, auth_repository: "AbstractAuthRepository"):
        cls._auth_repository = auth_repository

    @classmethod
    def get_task_repository(cls) -> "AbstractTaskRepository":
        return cls._task_repository

    @classmethod
    def set_task_repository(cls, task_repository: "AbstractTaskRepository"):
        cls._task_repository = task_repository

    @classmethod
    def get_machine_repository(cls) -> "AbstractMachineRepository":
        return cls._machine_repository

    @classmethod
    def set_machine_repository(cls, machine_repository: "AbstractMachineRepository"):
        cls._machine_repository = machine_repository

    @classmethod
    def get_agregate_repository(cls) -> "AbstractAgregateRepository":
        return cls._agregate_repository

    @classmethod
    def set_agregate_repository(cls, agregate_repository: "AbstractAgregateRepository"):
        cls._agregate_repository = agregate_repository


DEPENDS = Depends(lambda: Dependencies)
"""It's a dependency injection container for FastAPI.
See `FastAPI docs <(https://fastapi.tiangolo.com/tutorial/dependencies/)>`_ for more info"""
DEPENDS_STORAGE = Depends(Dependencies.get_storage)
DEPENDS_USER_REPOSITORY = Depends(Dependencies.get_user_repository)
DEPENDS_SMTP_REPOSITORY = Depends(Dependencies.get_smtp_repository)
DEPENDS_AUTH_REPOSITORY = Depends(Dependencies.get_auth_repository)
DEPENDS_TASK_REPOSITORY = Depends(Dependencies.get_task_repository)
DEPENDS_MACHINE_REPOSITORY = Depends(Dependencies.get_machine_repository)
DEPENDS_AGREGATE_REPOSITORY = Depends(Dependencies.get_agregate_repository)

from src.modules.auth.dependencies import verify_request  # noqa: E402

DEPENDS_VERIFIED_REQUEST = Depends(verify_request)

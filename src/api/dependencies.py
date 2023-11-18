__all__ = [
    "DEPENDS",
    "DEPENDS_SMTP_REPOSITORY",
    "DEPENDS_STORAGE",
    "DEPENDS_USER_REPOSITORY",
    "DEPENDS_VERIFIED_REQUEST",
    "DEPENDS_AUTH_REPOSITORY",
    "Dependencies",
]

from fastapi import Depends

from src.modules.smtp.abc import AbstractSMTPRepository
from src.modules.users.abc import AbstractUserRepository
from src.modules.auth.abc import AbstractTokenRepository, AbstractAuthRepository
from src.storages.sqlalchemy.storage import AbstractSQLAlchemyStorage


class Dependencies:
    _storage: "AbstractSQLAlchemyStorage"
    _user_repository: "AbstractUserRepository"
    _smtp_repository: "AbstractSMTPRepository"
    _auth_repository: "AbstractAuthRepository"


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


DEPENDS = Depends(lambda: Dependencies)
"""It's a dependency injection container for FastAPI.
See `FastAPI docs <(https://fastapi.tiangolo.com/tutorial/dependencies/)>`_ for more info"""
DEPENDS_STORAGE = Depends(Dependencies.get_storage)
DEPENDS_USER_REPOSITORY = Depends(Dependencies.get_user_repository)
DEPENDS_SMTP_REPOSITORY = Depends(Dependencies.get_smtp_repository)
DEPENDS_AUTH_REPOSITORY = Depends(Dependencies.get_auth_repository)

from src.modules.auth.dependencies import verify_request  # noqa: E402

DEPENDS_VERIFIED_REQUEST = Depends(verify_request)

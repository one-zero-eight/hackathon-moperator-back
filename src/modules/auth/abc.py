__all__ = ["AbstractTokenRepository", "AbstractAuthRepository"]

from abc import ABCMeta, abstractmethod

from src.modules.auth.schemas import VerificationResult
from src.modules.users.schemas import ViewUser


class AbstractTokenRepository(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create_access_token(cls, user_id: int) -> str:
        ...

    @classmethod
    @abstractmethod
    def verify_access_token(cls, auth_token: str) -> VerificationResult:
        ...


class AbstractAuthRepository(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        ...

    @classmethod
    @abstractmethod
    def get_password_hash(cls, password: str) -> str:
        ...

    @classmethod
    @abstractmethod
    async def authenticate_user(cls, password: str = None, login: str = None, tag: str = None) -> int:
        ...

    @classmethod
    @abstractmethod
    async def _get_user(cls, login: str = None, tag: str = None) -> ViewUser:
        ...

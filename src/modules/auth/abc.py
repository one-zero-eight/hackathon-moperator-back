__all__ = ["AbstractTokenRepository"]

from abc import ABCMeta, abstractmethod

from src.modules.auth.schemas import VerificationResult


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
    def verify_password(cls, plain_password, hashed_password) -> bool:
        ...

    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)


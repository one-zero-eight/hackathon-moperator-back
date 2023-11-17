__all__ = ["TokenRepository"]

from datetime import timedelta, datetime

from authlib.jose import jwt, JoseError

from src.api.dependencies import Dependencies
from src.config import settings
from src.modules.auth.abc import AbstractTokenRepository
from src.modules.auth.schemas import VerificationResult


class TokenRepository(AbstractTokenRepository):
    ALGORITHM = "HS256"

    @classmethod
    async def verify_access_token(cls, auth_token: str) -> VerificationResult:
        try:
            payload = jwt.decode(auth_token, settings.JWT_PUBLIC_KEY)
        except JoseError:
            return VerificationResult(success=False)

        user_repository = Dependencies.get_user_repository()
        user_id: str = payload.get("sub")

        if user_id is None or not user_id.isdigit():
            return VerificationResult(success=False)

        converted_user_id = int(user_id)

        if await user_repository.read(converted_user_id) is None:
            return VerificationResult(success=False)

        return VerificationResult(success=True, user_id=converted_user_id)

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        access_token = TokenRepository._create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(days=90),
        )
        return access_token

    @classmethod
    def _create_access_token(cls, data: dict, expires_delta: timedelta) -> str:
        payload = data.copy()
        issued_at = datetime.utcnow()
        expire = issued_at + expires_delta
        payload.update({"exp": expire, "iat": issued_at})
        encoded_jwt = jwt.encode(
            {"alg": cls.ALGORITHM}, payload, settings.JWT_PRIVATE_KEY
        )
        return str(encoded_jwt, "utf-8")

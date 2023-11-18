__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter

from src.api.dependencies import DEPENDS_AUTH_REPOSITORY
from src.modules.auth.abc import AbstractAuthRepository
from src.modules.auth.repository import TokenRepository
from src.modules.auth.schemas import AuthResult, EmailAuthCredentials, TagAuthCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])


# by-tag
@router.post("/by-credentials", response_model=AuthResult)
async def by_credentials(
    credentials: EmailAuthCredentials, auth_repository: Annotated[AbstractAuthRepository, DEPENDS_AUTH_REPOSITORY]
):
    user_id = await auth_repository.authenticate_user(password=credentials.password, login=credentials.login)
    token = TokenRepository.create_access_token(user_id)
    return AuthResult(token=token, success=True)


@router.post("/by-tag", response_model=AuthResult)
async def by_tag(
    credentials: TagAuthCredentials, auth_repository: Annotated[AbstractAuthRepository, DEPENDS_AUTH_REPOSITORY]
):
    user_id = await auth_repository.authenticate_user(tag=credentials.tag)
    token = TokenRepository.create_access_token(user_id)
    return AuthResult(token=token, success=True)

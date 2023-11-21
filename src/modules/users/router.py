__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import DEPENDS_USER_REPOSITORY
from src.api.exceptions import (
    IncorrectCredentialsException,
    NoCredentialsException,
)
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import ViewUser, Notification

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    responses={
        200: {"description": "All users"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_all(
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    verification: Annotated[VerificationResult, Depends(verify_request)],
) -> list[ViewUser]:
    """
    Get all users info
    """

    users = await user_repository.get_all()
    return users


@router.get(
    "/me",
    responses={
        200: {"description": "User info"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_me(
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    verification: Annotated[VerificationResult, Depends(verify_request)],
) -> ViewUser:
    """
    Get user info
    """

    user = await user_repository.read(verification.user_id)
    user: ViewUser
    return user


@router.get(
    "/my-notifications",
    responses={
        200: {"description": "Notifications"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_my_notifications(
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
    verification: Annotated[VerificationResult, Depends(verify_request)],
) -> list[Notification]:
    """
    Get user notifications
    """

    user_id = verification.user_id
    return user_repository.read_and_clear_notifications(user_id)


@router.get(
    "/{user_id}",
    responses={
        200: {"description": "User info"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_user(
    user_id: int,
    user_repository: Annotated[UserRepository, DEPENDS_USER_REPOSITORY],
) -> ViewUser:
    """
    Get user info
    """
    user = await user_repository.read(user_id)
    user: ViewUser
    return user

__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks

from src.api.dependencies import DEPENDS_SMTP_REPOSITORY, DEPENDS_USER_REPOSITORY
from src.config import settings
from src.api.exceptions import (
    IncorrectCredentialsException,
    NoCredentialsException,
)
from src.modules.auth.dependencies import verify_request
from src.modules.smtp.abc import AbstractSMTPRepository
from src.modules.users.abc import AbstractUserRepository
from src.modules.auth.schemas import VerificationResult
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
    user_repository: Annotated[AbstractUserRepository, DEPENDS_USER_REPOSITORY],
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
    user_repository: Annotated[AbstractUserRepository, DEPENDS_USER_REPOSITORY],
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
    user_repository: Annotated[AbstractUserRepository, DEPENDS_USER_REPOSITORY],
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
    user_repository: Annotated[AbstractUserRepository, DEPENDS_USER_REPOSITORY],
) -> ViewUser:
    """
    Get user info
    """
    user = await user_repository.read(user_id)
    user: ViewUser
    return user


if settings.SMTP_ENABLED:

    @router.post("/connect-email", tags=["Email"])
    async def connect_email(
        email: str,
        user_id: int,
        background_tasks: BackgroundTasks,
        smtp_repository: Annotated[AbstractSMTPRepository, DEPENDS_SMTP_REPOSITORY],
        user_repository: Annotated[AbstractUserRepository, DEPENDS_USER_REPOSITORY],
    ):
        """
        Start registration via email
        """

        email_flow = await user_repository.start_connect_email(user_id, email)
        background_tasks.add_task(smtp_repository.send_connect_email, email_flow.email, email_flow.auth_code)

    @router.post("/connect-email/finish", tags=["Email"])
    async def finish_connect_email(
        email: str,
        auth_code: str,
        user_repository: Annotated[AbstractUserRepository, DEPENDS_USER_REPOSITORY],
    ):
        """
        Finish registration via email
        """
        await user_repository.finish_connect_email(email=email, auth_code=auth_code)

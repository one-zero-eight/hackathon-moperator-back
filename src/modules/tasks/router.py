__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_mock import MockException

from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.tasks.schemas import ViewTask

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/my",
    responses={
        200: {"description": "Tasks list for current user"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_my_tasks(
    verification: Annotated[VerificationResult, Depends(verify_request)],
) -> list[ViewTask]:
    """
    Get tasks list for current user
    """

    raise MockException(list[ViewTask])


@router.get(
    "/{task_id}",
    responses={
        200: {"description": "Task info"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_task(
    task_id: int,
) -> ViewTask:
    """
    Get task info
    """

    raise MockException(ViewTask)


@router.post(
    "/{task_id}/status",
    responses={
        200: {"description": "Change task status"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def change_task_status(
    task_id: int,
    verification: Annotated[VerificationResult, Depends(verify_request)],
) -> ViewTask:
    """
    Change task status
    """

    raise MockException(ViewTask)

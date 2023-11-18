__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_mock import MockException

from src.api.dependencies import DEPENDS_TASK_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.tasks.abc import AbstractTaskRepository
from src.modules.tasks.schemas import ViewTask, ChangeTaskStatus

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
    task_repository: Annotated[AbstractTaskRepository, DEPENDS_TASK_REPOSITORY]
) -> list[ViewTask]:
    """
    Get tasks list for current user
    """
    tasks = await task_repository.get_user_tasks(verification.user_id)
    return tasks


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
    verification: Annotated[VerificationResult, Depends(verify_request)],
    task_repository: Annotated[AbstractTaskRepository, DEPENDS_TASK_REPOSITORY]
) -> ViewTask:
    """
    Get task info
    """
    task = await task_repository.get_task(task_id)
    return task


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
    status: ChangeTaskStatus,
    verification: Annotated[VerificationResult, Depends(verify_request)],
    task_repository: Annotated[AbstractTaskRepository, DEPENDS_TASK_REPOSITORY],
) -> ViewTask:
    """
    Change task status
    """
    task = await task_repository.change_task_status(task_id, status.status)
    return task

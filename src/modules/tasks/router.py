__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from src.api.dependencies import DEPENDS_TASK_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.tasks.abc import AbstractTaskRepository
from src.modules.tasks.schemas import ViewTask, ChangeTaskStatus, FlatViewTask

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/my",
    responses={
        200: {"description": "Tasks list for current user"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
    response_model_exclude_none=True,
)
async def get_my_tasks(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    task_repository: Annotated[AbstractTaskRepository, DEPENDS_TASK_REPOSITORY],
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
    task_repository: Annotated[AbstractTaskRepository, DEPENDS_TASK_REPOSITORY],
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
    response_model_exclude_none=True,
)
async def change_task_status(
    task_id: int,
    status: ChangeTaskStatus,
    verification: Annotated[VerificationResult, Depends(verify_request)],
    task_repository: Annotated[AbstractTaskRepository, DEPENDS_TASK_REPOSITORY],
) -> FlatViewTask:
    """
    Change task status
    """

    existing_task = await task_repository.get_task(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    #
    # if existing_task.asignee_id != verification.user_id:
    #     raise HTTPException(status_code=403, detail="You are not asignee of this task")

    task = await task_repository.change_task_status(task_id, status.status)
    return task

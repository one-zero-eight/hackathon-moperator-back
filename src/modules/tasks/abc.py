__all__ = ["AbstractTaskRepository"]

from abc import ABCMeta, abstractmethod
from typing import Optional

from src.modules.tasks.schemas import ViewTask


class AbstractTaskRepository(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def get_task(cls, task_id: int) -> Optional[ViewTask]:
        ...

    @classmethod
    @abstractmethod
    async def get_user_tasks(cls, user_id: int) -> Optional[list[ViewTask]]:
        ...

    @classmethod
    @abstractmethod
    async def change_task_status(cls, task_id: int, status: str) -> ViewTask:
        ...

__all__ = ["AbstractTaskRepository"]

from abc import ABCMeta, abstractmethod
from typing import Optional

from src.modules.tasks.schemas import FlatViewTask


class AbstractTaskRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_task(self, task_id: int) -> Optional[FlatViewTask]:
        ...

    @abstractmethod
    async def get_user_tasks(self, user_id: int) -> Optional[list[FlatViewTask]]:
        ...

    @abstractmethod
    async def change_task_status(self, task_id: int, status: str) -> FlatViewTask:
        ...

    @abstractmethod
    async def get_all(self) -> Optional[list[FlatViewTask]]:
        ...

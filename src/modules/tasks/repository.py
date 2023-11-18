__all__ = ["TaskRepository"]

from sqlalchemy import select
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.tasks.abc import AbstractTaskRepository
from src.modules.tasks.schemas import ViewTask
from src.storages.sqlalchemy import AbstractSQLAlchemyStorage
from src.storages.sqlalchemy.models import Task


class TaskRepository(AbstractTaskRepository):
    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    @classmethod
    async def get_task(cls, task_id: int) -> Optional[ViewTask]:
        async with cls._create_session() as session:
            q = select(Task).where(Task.id == task_id)
            task = await session.scalar(q)
            if task:
                return ViewTask.model_validate(task)

    @classmethod
    async def get_user_tasks(cls, user_id: int) -> Optional[list[ViewTask]]:
        pass

    @classmethod
    async def change_task_status(cls, task_id: int, status: str) -> ViewTask:
        pass

__all__ = ["TaskRepository"]

from sqlalchemy import select, update
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

    async def get_task(self, task_id: int) -> Optional[ViewTask]:
        async with self._create_session() as session:
            q = select(Task).where(Task.id == task_id)
            task = await session.scalar(q)
            if task:
                return ViewTask.model_validate(task)

    async def get_user_tasks(self, user_id: int) -> Optional[list[ViewTask]]:
        async with self._create_session() as session:
            q = select(Task).where(Task.asignee_id == user_id)
            tasks = await session.scalars(q)
            if tasks:
                return [ViewTask.model_validate(task) for task in tasks]

    async def change_task_status(self, task_id: int, status: str) -> ViewTask:
        async with self._create_session() as session:
            stmt = (update(Task).where(Task.id == task_id).values(status=status))
            await session.execute(stmt)
            await session.commit()

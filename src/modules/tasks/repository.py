__all__ = ["TaskRepository"]

from typing import Optional

from sqlalchemy import select, update

from src.api.exceptions import ObjectNotFound
from src.modules.tasks.schemas import FlatViewTask
from src.storages.sqlalchemy.models import Task
from src.storages.sqlalchemy.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    async def get_all(self) -> Optional[list[FlatViewTask]]:
        async with self._create_session() as session:
            q = select(Task)
            tasks = await session.scalars(q)
            if tasks:
                return [FlatViewTask.model_validate(task) for task in tasks]

    async def get_task(self, task_id: int) -> Optional[FlatViewTask]:
        async with self._create_session() as session:
            q = select(Task).where(Task.id == task_id)
            task = await session.scalar(q)
            if task is None:
                raise ObjectNotFound()
            return FlatViewTask.model_validate(task)

    async def get_user_tasks(self, user_id: int) -> Optional[list[FlatViewTask]]:
        async with self._create_session() as session:
            q = select(Task).where(Task.asignee_id == user_id)
            tasks = await session.scalars(q)
            if tasks:
                return [FlatViewTask.model_validate(task) for task in tasks]

    async def change_task_status(self, task_id: int, status: str) -> FlatViewTask:
        async with self._create_session() as session:
            stmt = update(Task).where(Task.id == task_id).values(status=status)
            await session.execute(stmt)
            await session.commit()
            q = select(Task).where(Task.id == task_id)
            task = await session.scalar(q)
            return FlatViewTask.model_validate(task)

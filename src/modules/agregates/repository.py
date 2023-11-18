__all__ = ["AgregateRepository"]

from sqlalchemy import select
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ObjectNotFound
from src.modules.agregates.abc import AbstractAgregateRepository
from src.modules.agregates.schemas import ViewAgregate
from src.storages.sqlalchemy import AbstractSQLAlchemyStorage
from src.storages.sqlalchemy.models import Agregate


class AgregateRepository(AbstractAgregateRepository):
    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def get_agregate(self, agregate_id: int) -> Optional[ViewAgregate]:
        async with self._create_session() as session:
            q = select(Agregate).where(Agregate.id == agregate_id)
            agregate = await session.scalar(q)
            if agregate is None:
                raise ObjectNotFound()
            return ViewAgregate.model_validate(agregate)

    async def get_all(self) -> Optional[list[ViewAgregate]]:
        async with self._create_session() as session:
            q = select(Agregate)
            agregates = await session.scalars(q)
            if agregates:
                return [ViewAgregate.model_validate(agregate) for agregate in agregates]

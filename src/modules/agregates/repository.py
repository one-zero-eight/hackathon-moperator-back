__all__ = ["AgregateRepository"]

from typing import Optional

from sqlalchemy import select

from src.api.exceptions import ObjectNotFound
from src.modules.agregates.schemas import ViewAgregate
from src.storages.sqlalchemy.models import Agregate
from src.storages.sqlalchemy.repository import SQLAlchemyRepository


class AgregateRepository(SQLAlchemyRepository):
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

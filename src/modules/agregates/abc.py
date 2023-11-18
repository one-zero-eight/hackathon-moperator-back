__all__ = ["AbstractAgregateRepository"]

from abc import ABCMeta, abstractmethod
from typing import Optional

from src.modules.agregates.schemas import ViewAgregate


class AbstractAgregateRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_agregate(self, agregate_id: int) -> Optional[ViewAgregate]:
        ...

    @abstractmethod
    async def get_all(self) -> Optional[list[ViewAgregate]]:
        ...


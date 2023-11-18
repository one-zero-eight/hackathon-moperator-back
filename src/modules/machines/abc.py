__all__ = ["AbstractMachineRepository"]

from abc import ABCMeta, abstractmethod
from typing import Optional

from src.modules.machines.schemas import ViewMachine


class AbstractMachineRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get_machine(self, machine_id: int) -> Optional[ViewMachine]:
        ...

    @abstractmethod
    async def get_all(self) -> Optional[list[ViewMachine]]:
        ...


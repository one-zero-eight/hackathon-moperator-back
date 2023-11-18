__all__ = ["MachineRepository"]

from sqlalchemy import select
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.machines.abc import AbstractMachineRepository
from src.modules.machines.schemas import ViewMachine
from src.storages.sqlalchemy import AbstractSQLAlchemyStorage
from src.storages.sqlalchemy.models import Machine


class MachineRepository(AbstractMachineRepository):
    def __init__(self, storage: AbstractSQLAlchemyStorage):
        self.storage = storage

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def get_machine(self, machine_id: int) -> Optional[ViewMachine]:
        async with self._create_session() as session:
            q = select(Machine).where(Machine.id == machine_id)
            machine = await session.scalar(q)
            if machine:
                return ViewMachine.model_validate(machine)

    async def get_all(self) -> Optional[list[ViewMachine]]:
        async with self._create_session() as session:
            q = select(Machine)
            machines = await session.scalars(q)
            if machines:
                return [ViewMachine.model_validate(machine) for machine in machines]

__all__ = ["MachineRepository"]

from sqlalchemy import select
from typing import Optional

from src.api.exceptions import ObjectNotFound
from src.modules.machines.schemas import ViewMachine
from src.storages.sqlalchemy.models import Machine
from src.storages.sqlalchemy.repository import SQLAlchemyRepository


class MachineRepository(SQLAlchemyRepository):
    async def get_machine(self, machine_id: int) -> Optional[ViewMachine]:
        async with self._create_session() as session:
            q = select(Machine).where(Machine.id == machine_id)
            machine = await session.scalar(q)
            if machine is None:
                raise ObjectNotFound()
            return ViewMachine.model_validate(machine)

    async def get_all(self) -> Optional[list[ViewMachine]]:
        async with self._create_session() as session:
            q = select(Machine)
            machines = await session.scalars(q)
            if machines:
                return [ViewMachine.model_validate(machine) for machine in machines]

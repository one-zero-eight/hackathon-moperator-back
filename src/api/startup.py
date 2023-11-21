from fastapi import FastAPI

from src.config import settings
from src.modules.agregates.repository import AgregateRepository
from src.modules.auth.repository import AuthRepository
from src.modules.machines.repository import MachineRepository
from src.modules.tasks.repository import TaskRepository


async def setup_repositories():
    from src.modules.users.repository import UserRepository
    from src.storages.sqlalchemy.storage import SQLAlchemyStorage
    from src.api.dependencies import Dependencies

    # ------------------- Repositories Dependencies -------------------
    storage = SQLAlchemyStorage.from_url(settings.DB_URL.get_secret_value())
    user_repository = UserRepository(storage)
    auth_repository = AuthRepository(storage)
    task_repository = TaskRepository(storage)
    machine_repository = MachineRepository(storage)
    agregate_repository = AgregateRepository(storage)

    Dependencies.set_auth_repository(auth_repository)
    Dependencies.set_storage(storage)
    Dependencies.set_user_repository(user_repository)
    Dependencies.set_task_repository(task_repository)
    Dependencies.set_machine_repository(machine_repository)
    Dependencies.set_agregate_repository(agregate_repository)

    # await storage.create_all()


def setup_admin(app: FastAPI):
    from src.modules.admin.app import init_app
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(settings.DB_URL.get_secret_value(), pool_recycle=3600)

    init_app(app, engine)

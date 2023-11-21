__all__ = ["UserRepository"]

import random
from collections import defaultdict
from typing import Optional

from sqlalchemy import select, insert

from src.modules.users.schemas import ViewUser, CreateUser, Notification
from src.storages.sqlalchemy.models.users import User
from src.storages.sqlalchemy.repository import SQLAlchemyRepository
from src.storages.sqlalchemy.storage import SQLAlchemyStorage


def _generate_auth_code() -> str:
    # return random 6-digit code
    return str(random.randint(100_000, 999_999))


class UserRepository(SQLAlchemyRepository):
    storage: SQLAlchemyStorage
    notifications: dict[int, list[Notification]]

    def __init__(self, storage: SQLAlchemyStorage):
        super().__init__(storage)
        self.notifications = defaultdict(list)

    async def get_all(self) -> list["ViewUser"]:
        async with self._create_session() as session:
            q = select(User)
            users = await session.scalars(q)
            if users:
                return [ViewUser.model_validate(user, from_attributes=True) for user in users]

    def add_notification(self, user_id: int, notification: Notification):
        self.notifications[user_id].append(notification)

    def read_and_clear_notifications(self, user_id: int) -> list[Notification]:
        notifications = self.notifications[user_id]
        self.notifications[user_id] = list()
        return notifications

    # ------------------ CRUD ------------------ #

    async def create(self, user: CreateUser) -> ViewUser:
        async with self._create_session() as session:
            q = insert(User).values(**user.model_dump()).returning(User)
            new_user = await session.scalar(q)
            await session.commit()
            return ViewUser.model_validate(new_user)

    async def read(self, id_: int) -> Optional["ViewUser"]:
        async with self._create_session() as session:
            q = select(User).where(User.user_id == id_)
            user = await session.scalar(q)
            if user:
                return ViewUser.model_validate(user, from_attributes=True)

    async def read_by_email(self, email: str) -> Optional["ViewUser"]:
        async with self._create_session() as session:
            q = select(User).where(User.email == email)
            user = await session.scalar(q)
            if user:
                return ViewUser.model_validate(user, from_attributes=True)

    # ^^^^^^^^^^^^^^^^^^^ CRUD ^^^^^^^^^^^^^^^^^^^ #

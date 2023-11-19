__all__ = ["AbstractUserRepository"]

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.users.schemas import ViewUser, CreateUser, ViewEmailFlow, Notification


class AbstractUserRepository(metaclass=ABCMeta):
    # ----------------- CRUD ----------------- #

    @abstractmethod
    def add_notification(self, user_id: int, notification: "Notification"):
        ...

    @abstractmethod
    def read_and_clear_notifications(self, user_id: int) -> list["Notification"]:
        ...

    @abstractmethod
    async def create(self, user: "CreateUser") -> "ViewUser":
        ...

    @abstractmethod
    async def read(self, id_: int) -> "ViewUser":
        ...

    @abstractmethod
    async def read_by_email(self, email: str) -> "ViewUser":
        ...

    @abstractmethod
    async def start_connect_email(self, id_: int, email: str) -> "ViewEmailFlow":
        ...

    @abstractmethod
    async def finish_connect_email(self, email: str, auth_code: str):
        ...

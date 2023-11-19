__all__ = ["User", "EmailFlow", "UserRoles"]

from typing import Optional

from fastapi_storages import FileSystemStorage
from sqlalchemy import Column

from src.storages.sqlalchemy.models.__mixin__ import IdMixin, NoneImageType
from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.utils import *

photo_storage = FileSystemStorage(path="./tmp")


class UserRoles(Base, IdMixin):
    __tablename__ = "user_role"
    name: Mapped[str] = mapped_column(unique=True)


class User(Base):
    __tablename__ = "user_data"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(unique=True, nullable=True)

    rfid_id: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(unique=True)

    last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    middle_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column()

    photo = Column(NoneImageType(storage=photo_storage), nullable=True)

    def __repr__(self):
        full_name = " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))
        return f"{full_name}: {self.role}"


class EmailFlow(Base, IdMixin):
    __tablename__ = "email_flows"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    user: Mapped[User] = relationship(User, backref="email_flows")

    auth_code: Mapped[str] = mapped_column(nullable=False)

    finished: Mapped[bool] = mapped_column(default=False)

    # unique constraint
    __table_args__ = (UniqueConstraint("email", "auth_code", name="email_auth_code_unique_constraint"),)

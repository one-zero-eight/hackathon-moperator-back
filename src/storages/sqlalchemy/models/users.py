__all__ = ["User", "EmailFlow", "UserRoles"]

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base


class UserRoles(Base, IdMixin):
    __tablename__ = "user_role"

    name: Mapped[str] = mapped_column(unique=True)


class User(Base):
    __tablename__ = "user_data"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    rfid_id: Mapped[str] = mapped_column(unique=True)

    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(unique=True)

    employee_id: Mapped[int] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()


class EmailFlow(Base, IdMixin):
    __tablename__ = "email_flows"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    user: Mapped[User] = relationship(User, backref="email_flows")

    auth_code: Mapped[str] = mapped_column(nullable=False)

    finished: Mapped[bool] = mapped_column(default=False)

    # unique constraint
    __table_args__ = (UniqueConstraint("email", "auth_code", name="email_auth_code_unique_constraint"),)

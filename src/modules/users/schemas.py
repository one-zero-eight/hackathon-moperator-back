__all__ = ["ViewUser", "CreateUser", "UpdateUser", "ViewEmailFlow", "UserCredentials"]

from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserRoles(StrEnum):
    agronomist = "agronomist"
    moperator = "moperator"
    admin = "admin"


class ViewUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    rfid_id: Optional[str] = None
    email: str
    employee_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    role: UserRoles

    @property
    def is_admin(self) -> bool:
        return self.role == UserRoles.admin or self.role == UserRoles.agronomist


class UserCredentials(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    password_hash: str


class CreateUser(BaseModel):
    rfid_id: Optional[str] = None
    email: str
    password: str
    role: UserRoles
    employee_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None


class UpdateUser(BaseModel):
    rfid_id: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    employee_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    role: Optional[UserRoles] = None


class ViewEmailFlow(BaseModel):
    email: str
    auth_code: str
    user_id: int

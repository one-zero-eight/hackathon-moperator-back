__all__ = ["ViewUser", "CreateUser", "ViewEmailFlow"]

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ViewUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    rfid_id: Optional[str] = None
    email: str
    employee_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    role: str


class UserCredentials(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    password_hash: str


class CreateUser(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class ViewEmailFlow(BaseModel):
    email: str
    auth_code: str
    user_id: int

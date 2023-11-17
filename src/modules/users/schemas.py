__all__ = ["ViewUser", "CreateUser", "ViewEmailFlow"]

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ViewUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None

    email: Optional[str] = None
    email_verified: Optional[bool] = None


class CreateUser(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class ViewEmailFlow(BaseModel):
    email: str
    auth_code: str
    user_id: int

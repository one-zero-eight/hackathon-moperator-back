__all__ = ["VerificationResult", "AuthResult", "EmailAuthCredentials", "TagAuthCredentials"]

from typing import Optional

from pydantic import BaseModel


class VerificationResult(BaseModel):
    success: bool
    user_id: Optional[int] = None


class AuthResult(BaseModel):
    success: bool
    token: Optional[str] = None


class EmailAuthCredentials(BaseModel):
    login: str
    password: str


class TagAuthCredentials(BaseModel):
    tag: str

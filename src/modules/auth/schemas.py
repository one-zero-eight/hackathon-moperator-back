__all__ = ["VerificationResult", "AuthResult", "AuthCredentials", "AuthTag"]

from typing import Optional

from pydantic import BaseModel


class VerificationResult(BaseModel):
    success: bool
    user_id: Optional[int] = None


class AuthResult(BaseModel):
    success: bool
    token: Optional[str] = None
    token_type: Optional[str] = None
    user_id: Optional[int] = None


class AuthCredentials(BaseModel):
    login: str
    password: str


class AuthCredentials(BaseModel):
    tag: str

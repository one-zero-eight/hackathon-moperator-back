__all__ = ["VerificationResult"]

from typing import Optional

from pydantic import BaseModel


class VerificationResult(BaseModel):
    success: bool
    user_id: Optional[int] = None

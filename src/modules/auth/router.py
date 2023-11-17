__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies import DEPENDS_SMTP_REPOSITORY, DEPENDS_USER_REPOSITORY, DEPEND, DEPENDS_TOKEN_REPOSITORY
from src.api.exceptions import NoCredentialsException, IncorrectCredentialsException
from src.config import settings

from src.modules.smtp.abc import AbstractSMTPRepository
from src.modules.auth.abc import AbstractTokenRepository
from src.modules.auth.schemas import VerificationResult, AuthResult, AuthCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])


# by-tag
@router.post("/by-credentials", response_model=AuthResult)
async def by_credentials(
    credentials: AuthCredentials,
    token_repository: Annotated[AbstractTokenRepository, DEPENDS_TOKEN_REPOSITORY],
):
    user = token_repository.create_access_token()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
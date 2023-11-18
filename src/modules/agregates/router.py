__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import DEPENDS_AGREGATE_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.agregates.abc import AbstractAgregateRepository
from src.modules.agregates.schemas import ViewAgregate

router = APIRouter(prefix="/agregates", tags=["Agregates"])


@router.get(
    "/",
    responses={
        200: {"description": "Agregates list"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
    response_model_exclude_none=True,
)
async def get_all(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    agregate_repository: Annotated[AbstractAgregateRepository, DEPENDS_AGREGATE_REPOSITORY],
) -> list[ViewAgregate]:
    """
    Get agregates list
    """
    agregates = await agregate_repository.get_all()
    return agregates


@router.get(
    "/{agregate_id}",
    responses={
        200: {"description": "Agregate info"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_agregate(
    agregate_id: int,
    verification: Annotated[VerificationResult, Depends(verify_request)],
    agregate_repository: Annotated[AbstractAgregateRepository, DEPENDS_AGREGATE_REPOSITORY],
) -> ViewAgregate:
    """
    Get machine info
    """
    agregate = await agregate_repository.get_agregate(agregate_id)
    return agregate

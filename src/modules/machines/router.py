__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import DEPENDS_MACHINE_REPOSITORY
from src.api.exceptions import IncorrectCredentialsException, NoCredentialsException
from src.modules.auth.dependencies import verify_request
from src.modules.auth.schemas import VerificationResult
from src.modules.machines.abc import AbstractMachineRepository
from src.modules.machines.schemas import ViewMachine

router = APIRouter(prefix="/machines", tags=["Machines"])


@router.get(
    "/",
    responses={
        200: {"description": "Machines list"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
    response_model_exclude_none=True,
)
async def get_all(
    verification: Annotated[VerificationResult, Depends(verify_request)],
    machine_repository: Annotated[AbstractMachineRepository, DEPENDS_MACHINE_REPOSITORY],
) -> list[ViewMachine]:
    """
    Get machines list
    """
    machines = await machine_repository.get_all()
    return machines


@router.get(
    "/{machine_id}",
    responses={
        200: {"description": "Machine info"},
        **IncorrectCredentialsException.responses,
        **NoCredentialsException.responses,
    },
)
async def get_machine(
    machine_id: int,
    verification: Annotated[VerificationResult, Depends(verify_request)],
    machine_repository: Annotated[AbstractMachineRepository, DEPENDS_MACHINE_REPOSITORY],
) -> ViewMachine:
    """
    Get machine info
    """
    machine = await machine_repository.get_machine(machine_id)
    return machine

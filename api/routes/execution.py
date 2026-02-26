"""Endpoints F3 - Execucao em tempo real.

Requisitos: SYS-FR-020, SYS-FR-021, SYS-FR-022, SYS-FR-023, SYS-FR-024, SYS-FR-025
"""

from fastapi import APIRouter


router = APIRouter()


@router.post("/start")
async def start_execution() -> dict[str, str]:
    """Inicia a execucao do scheduler de estrategias."""
    return {"message": "Endpoint sera implementado no proximo incremento (F3)"}


@router.post("/stop")
async def stop_execution() -> dict[str, str]:
    """Para a execucao do scheduler."""
    return {"message": "Endpoint sera implementado no proximo incremento (F3)"}


@router.get("/status")
async def execution_status() -> dict[str, str]:
    """Retorna o status atual da execucao."""
    return {"message": "Endpoint sera implementado no proximo incremento (F3)"}


@router.post("/run-cycle")
async def run_single_cycle() -> dict[str, str]:
    """Executa um unico ciclo de estrategias (manual)."""
    return {"message": "Endpoint sera implementado no proximo incremento (F3)"}
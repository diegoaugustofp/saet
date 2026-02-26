"""Endpoints F1 - Gestao de ambientes de execucao.

Requisitos: SYS-FR-001, SYS-FR-002, SYS-FR-003
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_environments() -> dict[str, str]:
    """Lista ambientes configurados."""
    return {"message": "Endpoint sera implementado no proximo incremento (F1)"}


@router.post("/")
async def create_environment() -> dict[str, str]:
    """Configura um novo ambiente de execucao."""
    return {"message": "Endpoint sera implementado no proximo incremento (F1)"}


@router.post("/{account_id}/connect")
async def connect_environment(account_id: str) -> dict[str, str]:
    """Conecta a um ambiente de execucao."""
    return {"message": f"Conexao ao ambiente {account_id} sera implementada no incremento F1"}


@router.post("/{account_id}/select")
async def select_environment(account_id: str) -> dict[str, str]:
    """Seleciona um ambiente como ativo."""
    return {"message": f"Selecao do ambiente {account_id} sera implementada no incremento F1"}
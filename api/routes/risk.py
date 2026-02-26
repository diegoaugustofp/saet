"""Endpoints F7 - Gestao de risco por conta.

Requisitos: SYS-FR-060, SYS-NFR-050
"""

from fastapi import APIRouter
router = APIRouter()


@router.get("/{account_id}")
async def get_risk_config(account_id: str) -> dict[str, str]:
    """Retorna configuracao de risco de uma conta."""
    return {"message": f"Risco da conta {account_id} - incremento F7"}


@router.put("/{account_id}")
async def update_risk_config(account_id: str) -> dict[str, str]:
    """Atualiza limites de risco de uma conta."""
    return {"message": f"Atualizacao de risco da conta {account_id} - incremento F7"}
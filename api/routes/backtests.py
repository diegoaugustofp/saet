"""Endpoints F4 - Backtest e simulacao.

Requisitos: SYS-FR-030, SYS-FR-031, SYS-FR-032
"""
from fastapi import APIRouter

router = APIRouter()
@router.post("/")
async def run_backtest() -> dict[str, str]:  
    """Executa um backtest de estrategia."""
    return {"message": "Endpoint sera implementado no proximo incremento (F4)"}


@router.get("/{run_id}")
async def get_backtest_run(run_id: str) -> dict[str, str]:  
    """Retorna detalhes de uma execucao de backtest."""
    return {"message": f"Detalhes do backtest {run_id} - incremento F4"}


@router.get("/{run_id}/results")
async def get_backtest_results(run_id: str) -> dict[str, str]: 
    """Retorna resultados de um backtest."""
    return {"message": f"Resultados do backtest {run_id} - incremento F4"}


@router.get("/strategy/{strategy_id}")
async def list_backtests_by_strategy(strategy_id: str) -> dict[str, str]:
    """Lista backtests de uma estrategia."""
    return {"message": f"Backtests da estrategia {strategy_id} - incremento F4"}

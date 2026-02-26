"""F5 - Servico de analise de performance e calibragem.

Responsavel por calcular metricas, comparar calibracoes de parametros
e marcar combinacoes validadas.

Requisitos: SYS-FR-040, SYS-FR-041, SYS-FR-042
Caso de uso: UC-05
"""

from datetime import datetime
from typing import Any
import structlog
from saet.core.domain.interfaces.repositories import BacktestRepository, StrategyRepository
from saet.core.domain.models.backtest import BacktestResult

logger = structlog.get_logger()

class PerformanceService:
    """Servico de analise de performance e calibragem."""
    
    def __init__(
        self,
        backtest_repository: BacktestRepository,
        strategy_repository: StrategyRepository,
    ) -> None:
        self._backtest_repo = backtest_repository
        self._strategy_repo = strategy_repository
    
    
    async def get_results_by_strategy(self, strategy_id: str) -> list[BacktestResult]:
        """Retorna todos os resultados de backtest de uma estrategia."""
        runs = await self._backtest_repo.list_runs_by_strategy(strategy_id)
        results: list[BacktestResult] = []
        for run in runs:
            run_results = await self._backtest_repo.get_results_by_run(run.id)
            results.extend(run_results)
        return results
    
    
    async def compare_calibrations(
        self, result_ids: list[str]
    ) -> list[dict[str, Any]]:
        """Compara diferentes calibracoes lado a lado.
    
        Args:
            result_ids: IDs dos resultados de backtest a comparar.
    
        Returns:
            Lista de dicionarios com metricas de cada calibracao.
        """
    
        comparisons: list[dict[str, Any]] = []
        for result_id in result_ids:
            # Buscar o resultado e o run associado
            for strategy in await self._strategy_repo.list_all():
                runs = await self._backtest_repo.list_runs_by_strategy(strategy.id)
                for run in runs:
                    results = await self._backtest_repo.get_results_by_run(run.id)
                    for result in results:
                        if result.id == result_id:
                            comparisons.append({
                                "result_id": result.id,
                                "strategy_name": strategy.name,
                                "parameters": run.parameters,
                                "period": f"{run.period_start} - {run.period_end}",
                                "symbol": run.symbol,
                                "total_return": result.total_return,
                                "max_drawdown": result.max_drawdown,
                                "sharpe_ratio": result.sharpe_ratio,
                                "win_rate": result.win_rate,
                                "avg_payoff": result.avg_payoff,
                                "total_trades": result.total_trades,
                                "validated": result.validated,
                            })
    
        return comparisons
    
    
    async def validate_result(
        self,
        result_id: str,
        validated_by: str,
    ) -> BacktestResult | None:
        """Marca um resultado de backtest como validado.
    
        Args:
            result_id: ID do resultado a ser validado.
            validated_by: Usuario que esta validando.
    
        Returns:
            Resultado atualizado ou None se nao encontrado.
        """
    
        # Buscar resultado em todos os runs
        for strategy in await self._strategy_repo.list_all():
            runs = await self._backtest_repo.list_runs_by_strategy(strategy.id)
            for run in runs:
                results = await self._backtest_repo.get_results_by_run(run.id)
                for result in results:
                    if result.id == result_id:
                        result.validated = True
                        result.validated_by = validated_by
                        result.validated_at = datetime.utcnow()
                        saved = await self._backtest_repo.save_result(result)
                        logger.info(
                            "result_validated",
                            result_id=result_id,
                            validated_by=validated_by,
                        )
                        return saved
    
        return None
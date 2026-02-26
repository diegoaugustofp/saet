"""F4 - Motor de backtest.

Responsavel por executar backtests de estrategias em dados historicos,
com cenarios variaveis e registro de resultados.

Requisitos: SYS-FR-030, SYS-FR-031, SYS-FR-032
Caso de uso: UC-04
"""

from datetime import datetime
from typing import Any

import structlog

from saet.core.domain.enums import SignalType
from saet.core.domain.interfaces.market_data import MarketDataProvider
from saet.core.domain.interfaces.repositories import BacktestRepository
from saet.core.domain.interfaces.strategy_runner import StrategyRunner
from saet.core.domain.models.backtest import BacktestResult, BacktestRun
from saet.core.domain.models.position import Position


logger = structlog.get_logger()


class BacktestEngine:
    """Motor de execucao de backtests."""
    
    def __init__(
        self,
        market_data: MarketDataProvider,
        backtest_repository: BacktestRepository,
    ) -> None:
        self._market_data = market_data
        self._backtest_repo = backtest_repository
    
    
    async def run_backtest(
        self,
        runner: StrategyRunner,
        strategy_id: str,
        symbol: str,
        timeframe: str,
        period_start: datetime,
        period_end: datetime,
        parameters: dict[str, Any],
    ) -> BacktestResult:
        """Executa um backtest de uma estrategia em dados historicos.
 
        Args:
            runner: Runner da estrategia a ser testada.
            strategy_id: ID da estrategia.
            symbol: Ativo para backtest.
            timeframe: Timeframe dos candles.
            period_start: Inicio do periodo de backtest.
            period_end: Fim do periodo de backtest.
            parameters: Parametros da estrategia para este cenario.
 
        Returns:
            Resultado do backtest com metricas calculadas.
        """
        
        runner.set_parameters(parameters)
        run = BacktestRun(
            strategy_id=strategy_id,
            parameters=parameters,
            period_start=period_start,
            period_end=period_end,
            symbol=symbol,
            timeframe=timeframe,
        )
        
        saved_run = await self._backtest_repo.save_run(run)
        candles = await self._market_data.get_candles(symbol, timeframe, period_start, period_end)
        logger.info(
            "backtest_started",
            strategy_id=strategy_id,
            symbol=symbol,
            candles_count=len(candles),
            period=f"{period_start} - {period_end}",
        )
        
        trades: list[dict[str, Any]] = []
        current_position: Position | None = None
        for candle in candles:
            signal = runner.on_candle(candle, current_position)
            if signal.signal_type == SignalType.BUY and current_position is None:
                current_position = Position(
                    symbol=symbol,
                    strategy_id=strategy_id,
                    entry_price=candle.close,
                    volume=signal.volume or 1.0,
                )
            elif signal.signal_type == SignalType.SELL and current_position is not None:
                pnl = (candle.close - current_position.entry_price) * current_position.volume
                trades.append({
                    "entry_price": current_position.entry_price,
                    "exit_price": candle.close,
                    "volume": current_position.volume,
                    "pnl": pnl,
                    "entry_time": current_position.opened_at.isoformat(),
                    "exit_time": candle.timestamp.isoformat(),
                })
                current_position = None
            elif signal.signal_type == SignalType.CLOSE and current_position is not None:
                pnl = (candle.close - current_position.entry_price) * current_position.volume
                trades.append({
                    "entry_price": current_position.entry_price,
                    "exit_price": candle.close,
                    "volume": current_position.volume,
                    "pnl": pnl,
                    "entry_time": current_position.opened_at.isoformat(),
                    "exit_time": candle.timestamp.isoformat(),
                })
                current_position = None
        
        metrics = self._calculate_metrics(trades)
        
        result = BacktestResult(
            run_id=saved_run.id,
            metrics=metrics,
            total_trades=len(trades),
            winning_trades=sum(1 for t in trades if t["pnl"] > 0),
            losing_trades=sum(1 for t in trades if t["pnl"] <= 0),
            total_return=metrics.get("total_return", 0.0),
            max_drawdown=metrics.get("max_drawdown", 0.0),
            sharpe_ratio=metrics.get("sharpe_ratio", 0.0),
            win_rate=metrics.get("win_rate", 0.0),
            avg_payoff=metrics.get("avg_payoff", 0.0),
        )
        saved_result = await self._backtest_repo.save_result(result)
        
        logger.info(
            "backtest_completed",
            strategy_id=strategy_id,
            symbol=symbol,
            total_trades=result.total_trades,
            total_return=result.total_return,
        )
        
        return saved_result
    
    
    @staticmethod
    def _calculate_metrics(trades: list[dict[str, Any]]) -> dict[str, Any]:
        """Calcula metricas de performance a partir dos trades."""
        
        if not trades:
            return {
                "total_return": 0.0,
                "max_drawdown": 0.0,
                "sharpe_ratio": 0.0,
                "win_rate": 0.0,
                "avg_payoff": 0.0,
            }
        pnls = [t["pnl"] for t in trades]
        total_return = sum(pnls)
        winning = [p for p in pnls if p > 0]
        losing = [p for p in pnls if p <= 0]
        win_rate = len(winning) / len(trades) if trades else 0.0
        avg_payoff = total_return / len(trades) if trades else 0.0
        
        # Calculo simplificado de drawdown
        cumulative = 0.0
        peak = 0.0
        max_drawdown = 0.0
        for pnl in pnls:
            cumulative += pnl
            if cumulative > peak:
                peak = cumulative
            drawdown = peak - cumulative
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Sharpe ratio simplificado (sem risk-free rate)
        import statistics
        
        if len(pnls) > 1:
            mean_return = statistics.mean(pnls)
            std_return = statistics.stdev(pnls)
            sharpe_ratio = mean_return / std_return if std_return > 0 else 0.0
        else:
            sharpe_ratio = 0.0
        
        return {
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "win_rate": win_rate,
            "avg_payoff": avg_payoff,
            "total_winning": sum(winning),
            "total_losing": sum(losing),
            "avg_winning": statistics.mean(winning) if winning else 0.0,
            "avg_losing": statistics.mean(losing) if losing else 0.0,
        }
"""Modelo de dominio: BacktestRun e BacktestResult."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

@dataclass
class BacktestRun:
    """Execucao de um backtest."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    strategy_id: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=datetime.utcnow)
    symbol: str = ""
    timeframe: str = "5m"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BacktestResult:
    """Resultado de um cenario de backtest."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    run_id: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0
    avg_payoff: float = 0.0
    validated: bool = False
    validated_by: str | None = None
    validated_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
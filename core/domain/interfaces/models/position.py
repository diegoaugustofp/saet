"""Modelo de dominio: Position."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from saet.core.domain.enums import PositionStatus


@dataclass
class Position:
    """Posicao aberta ou fechada em um ativo."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    symbol: str = ""
    strategy_id: str = ""
    account_id: str = ""
    entry_price: float = 0.0
    current_price: float = 0.0
    volume: float = 0.0
    stop_loss: float | None = None
    take_profit: float | None = None
    status: PositionStatus = PositionStatus.OPEN
    pnl: float = 0.0
    opened_at: datetime = field(default_factory=datetime.utcnow)
    closed_at: datetime | None = None
"""Modelo de dominio: Signal."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4
from saet.core.domain.enums import SignalType


@dataclass
class Signal:
    """Sinal gerado por uma estrategia."""
    id: str = field(default_factory=lambda: str(uuid4()))
    strategy_id: str = ""
    symbol: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    signal_type: SignalType = SignalType.HOLD
    price: float = 0.0
    volume: float = 0.0
    stop_loss: float | None = None
    take_profit: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
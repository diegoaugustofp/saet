"""Modelo de dominio: Order."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4
from saet.core.domain.enums import OrderStatus, OrderType


@dataclass
class Order:
    """Ordem enviada ao broker."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    signal_id: str = ""
    symbol: str = ""
    order_type: OrderType = OrderType.MARKET_BUY
    volume: float = 0.0
    price: float = 0.0
    stop_loss: float | None = None
    take_profit: float | None = None
    status: OrderStatus = OrderStatus.PENDING
    mt5_ticket: int | None = None
    broker_response: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
"""Enumeracoes do dominio SAET."""


from enum import Enum


class Environment(str, Enum):
    """Ambiente de execucao."""
    BACKTEST = "backtest"
    DEMO = "demo"
    REAL = "real"


class SignalType(str, Enum):
    """Tipo de sinal gerado por uma estrategia."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE = "close"

class OrderType(str, Enum):
    """Tipo de ordem enviada ao broker."""
    MARKET_BUY = "market_buy"
    MARKET_SELL = "market_sell"
    LIMIT_BUY = "limit_buy"
    LIMIT_SELL = "limit_sell"


class OrderStatus(str, Enum):
    """Status de uma ordem."""
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PositionStatus(str, Enum):
    """Status de uma posicao."""
    OPEN = "open"
    CLOSED = "closed"


class StrategyStatus(str, Enum):
    """Status de uma estrategia em um ambiente."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    VALIDATED = "validated"


class Timeframe(str, Enum):
    """Timeframes suportados."""
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
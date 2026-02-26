"""Modelo de dominio: dados de mercado."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    """Representacao de um candle (barra de preco)."""
    
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: str = "5m"
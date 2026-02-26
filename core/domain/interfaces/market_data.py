"""Interface (port) para dados de mercado."""

from abc import ABC, abstractmethod
from datetime import datetime
from saet.core.domain.models.market import Candle


class MarketDataProvider(ABC):
    """Interface abstrata para obtencao de dados de mercado.
    Implementacoes concretas:
    - MT5MarketData: dados live via MetaTrader5
    - HistoricalMarketData: dados historicos para backtests
    """
    
    @abstractmethod
    async def get_latest_candle(self, symbol: str, timeframe: str) -> Candle:
        """Retorna o candle mais recente de um ativo."""
        ...
    
    
    @abstractmethod
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
        """Retorna candles historicos de um ativo em um periodo."""
        ...
    
    
    @abstractmethod
    async def get_current_price(self, symbol: str) -> float:
        """Retorna o preco atual de um ativo."""
        ...
    
    
    @abstractmethod
    async def get_available_symbols(self) -> list[str]:
        """Retorna lista de ativos disponiveis."""
        ...
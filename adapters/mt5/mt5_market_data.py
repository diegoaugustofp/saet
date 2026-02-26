"""Adapter: dados de mercado via MetaTrader 5.
Implementacao concreta de MarketDataProvider usando o SDK MT5.
"""

from datetime import datetime
import structlog
from saet.core.domain.interfaces.market_data import MarketDataProvider
from saet.core.domain.models.market import Candle
from .mt5_connection import MT5Connection

logger = structlog.get_logger()

class MT5MarketData(MarketDataProvider):
    """Provider de dados de mercado via MetaTrader 5."""
    
    def __init__(self, connection: MT5Connection) -> None:
        self._connection = connection
    
    
    async def get_latest_candle(self, symbol: str, timeframe: str) -> Candle:
        
        """Retorna o candle mais recente de um ativo via MT5."""
        
        if not await self._connection.ensure_connected():
            raise ConnectionError("Nao foi possivel conectar ao MT5")
        
        # NOTE: Implementacao real usaria mt5.copy_rates_from_pos()
        # import MetaTrader5 as mt5
        # timeframe_map = {"5m": mt5.TIMEFRAME_M5, ...}
        # rates = mt5.copy_rates_from_pos(symbol, timeframe_map[timeframe], 0, 1)
        raise NotImplementedError("get_latest_candle sera implementado no proximo incremento")
    
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
    
    
        """Retorna candles historicos de um ativo via MT5."""
        if not await self._connection.ensure_connected():
            raise ConnectionError("Nao foi possivel conectar ao MT5")
        
        # NOTE: Implementacao real usaria mt5.copy_rates_range()
        raise NotImplementedError("get_candles sera implementado no proximo incremento")
    
    
    async def get_current_price(self, symbol: str) -> float:
        
        """Retorna o preco atual de um ativo via MT5."""
        
        if not await self._connection.ensure_connected():
            raise ConnectionError("Nao foi possivel conectar ao MT5")
        
        # NOTE: Implementacao real usaria mt5.symbol_info_tick()
        raise NotImplementedError("get_current_price sera implementado no proximo incremento")
    
    
    async def get_available_symbols(self) -> list[str]:
        
        """Retorna lista de ativos disponiveis no MT5."""
        if not await self._connection.ensure_connected():
            raise ConnectionError("Nao foi possivel conectar ao MT5")
        
        # NOTE: Implementacao real usaria mt5.symbols_get()
        raise NotImplementedError("get_available_symbols sera implementado no proximo incremento")
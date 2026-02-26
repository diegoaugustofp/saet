"""Classe base para estrategias de trading.

Toda estrategia deve herdar de StrategyBase e implementar
os metodos on_candle() e get_parameters().

Requisito: SYS-NFR-030 (desacoplamento de estrategias).
"""

from abc import abstractmethod
from typing import Any
from saet.core.domain.interfaces.strategy_runner import StrategyRunner
from saet.core.domain.models.market import Candle
from saet.core.domain.models.position import Position
from saet.core.domain.models.trading_signal import Signal


class StrategyBase(StrategyRunner):
    """Classe base concreta para estrategias de trading.

    Herda de StrategyRunner (interface do dominio) e fornece
    implementacoes padrao para metodos utilitarios.

    Exemplo de uso:
        class MinhaEstrategia(StrategyBase):
            @property
            def name(self) -> str:
                return "Minha Estrategia"

            @property
            def description(self) -> str:
                return "Descricao da estrategia"

            def on_candle(self, candle, position):
                # Logica de decisao
                return Signal(signal_type=SignalType.HOLD)

            def get_parameters(self) -> dict:
                return self._parameters

            def set_parameters(self, parameters: dict) -> None:
                self._parameters = parameters
    """
    
    
    def __init__(self, parameters: dict[str, Any] | None = None) -> None:
        self._parameters: dict[str, Any] = parameters or {}
    
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome da estrategia."""
        ...
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Descricao da estrategia."""
        ...
        
    @abstractmethod
    def on_candle(self, candle: Candle, position: Position | None) -> Signal:
        """Logica principal da estrategia."""
        ...
    
    def get_parameters(self) -> dict[str, Any]:
        """Retorna os parametros da estrategia."""
        return dict(self._parameters)
    
    def set_parameters(self, parameters: dict[str, Any]) -> None:
        """Define os parametros da estrategia."""
        self._parameters = dict(parameters)
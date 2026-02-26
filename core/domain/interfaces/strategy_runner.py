"""Interface (port) base para estrategias de trading."""

from abc import ABC, abstractmethod
from typing import Any
from saet.core.domain.models.market import Candle
from saet.core.domain.models.position import Position
from saet.core.domain.models.trading_signal import Signal


class StrategyRunner(ABC):
    """Interface abstrata que toda estrategia de trading deve implementar.
    Cada estrategia e um modulo Python que herda de StrategyRunner,
    implementando on_candle() e get_parameters().
    Isso garante o desacoplamento (SYS-NFR-030).
    """
    
    @abstractmethod
    def on_candle(
        self,
        candle: Candle,
        position: Position | None,
    ) -> Signal:
        """Recebe um candle e a posicao atual, retorna um sinal.
        Args:
            candle: Dados do candle atual.
            position: Posicao aberta atual no ativo, se houver.
        Returns:
            Signal com o tipo de acao (BUY, SELL, HOLD, CLOSE).
        """
        ...
    
    
    @abstractmethod
    def get_parameters(self) -> dict[str, Any]:
        """Retorna os parametros configurados da estrategia."""
        ...
    
    
    @abstractmethod
    def set_parameters(self, parameters: dict[str, Any]) -> None:
        """Define os parametros da estrategia."""
        ...
    
    
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
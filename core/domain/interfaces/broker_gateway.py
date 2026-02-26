"""Interface (port) para gateway do broker."""

from abc import ABC, abstractmethod
from saet.core.domain.models.order import Order
from saet.core.domain.models.position import Position


class BrokerGateway(ABC):
    """Interface abstrata para envio de ordens e gestao de posicoes no broker.
    Implementacoes concretas:
    - MT5BrokerGateway: ordens reais via MetaTrader5
    - BacktestBrokerGateway: simulacao para backtests
    """
    @abstractmethod
    async def send_order(self, order: Order) -> Order:
        """Envia uma ordem ao broker e retorna a ordem atualizada com status."""
        ...
    
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> Order:
        """Cancela uma ordem pendente."""
        ...
    
    
    @abstractmethod
    async def get_positions(self, symbol: str | None = None) -> list[Position]:
        """Retorna posicoes abertas, opcionalmente filtradas por ativo."""
        ...
    
    
    @abstractmethod
    async def close_position(self, position_id: str) -> Position:
        """Fecha uma posicao aberta."""
        ...
    
    
    @abstractmethod
    async def modify_position(
        self,
        position_id: str,
        stop_loss: float | None = None,
        take_profit: float | None = None,
    ) -> Position:
        """Modifica stop loss e/ou take profit de uma posicao."""
        ...
"""Interfaces (ports) de repositorios para persistencia."""

from abc import ABC, abstractmethod
from datetime import datetime
from saet.core.domain.models.account import Account, RiskConfig
from saet.core.domain.models.backtest import BacktestResult, BacktestRun
from saet.core.domain.models.order import Order
from saet.core.domain.models.position import Position
from saet.core.domain.models.trading_signal import Signal
from saet.core.domain.models.strategy import Strategy, StrategyVersion


class StrategyRepository(ABC):
    """Repositorio para estrategias."""
    
    @abstractmethod
    async def save(self, strategy: Strategy) -> Strategy:
        ...
    
    
    @abstractmethod
    async def get_by_id(self, strategy_id: str) -> Strategy | None:
        ...
    
    
    @abstractmethod
    async def list_all(self) -> list[Strategy]:
        ...
    
    
    @abstractmethod
    async def delete(self, strategy_id: str) -> None:
        ...
    
    
    @abstractmethod
    async def save_version(self, version: StrategyVersion) -> StrategyVersion:
        ...
    
    
    @abstractmethod
    async def get_versions(self, strategy_id: str) -> list[StrategyVersion]:
        ...


class AccountRepository(ABC):
    """Repositorio para contas de trading."""
    
    @abstractmethod
    async def save(self, account: Account) -> Account:
        ...
    
    
    @abstractmethod
    async def get_by_id(self, account_id: str) -> Account | None:
        ...
    
    
    @abstractmethod
    async def list_all(self) -> list[Account]:
        ...
    
    
    @abstractmethod
    async def delete(self, account_id: str) -> None:
        ...
    
    
    @abstractmethod
    async def save_risk_config(self, config: RiskConfig) -> RiskConfig:
        ...
    
    
    @abstractmethod
    async def get_risk_config(self, account_id: str) -> RiskConfig | None:
        ...


class OrderRepository(ABC):
    """Repositorio para ordens."""
    
    @abstractmethod
    async def save(self, order: Order) -> Order:
        ...
    
    
    @abstractmethod
    async def get_by_id(self, order_id: str) -> Order | None:
        ...
    
    
    @abstractmethod
    async def list_by_symbol(self, symbol: str) -> list[Order]:
        ...
    
    
    @abstractmethod
    async def list_by_strategy(self, strategy_id: str) -> list[Order]:
        ...


class PositionRepository(ABC):
    """Repositorio para posicoes."""
    
    @abstractmethod
    async def save(self, position: Position) -> Position:
        ...
    
    
    @abstractmethod
    async def get_by_id(self, position_id: str) -> Position | None:
        ...
    
    
    @abstractmethod
    async def get_open_by_symbol(self, symbol: str) -> Position | None:
        ...
    
    
    @abstractmethod
    async def list_open(self) -> list[Position]:
        ...
    
    
    @abstractmethod
    async def list_by_strategy(self, strategy_id: str) -> list[Position]:
        ...


class SignalRepository(ABC):
    """Repositorio para sinais."""
    
    @abstractmethod
    async def save(self, signal: Signal) -> Signal:
        ...
    
    
    @abstractmethod
    async def list_by_strategy(
        self, strategy_id: str, start: datetime | None = None, end: datetime | None = None
    ) -> list[Signal]:
        ...


class BacktestRepository(ABC):
    """Repositorio para backtests."""
    
    @abstractmethod
    async def save_run(self, run: BacktestRun) -> BacktestRun:
        ...
    
    
    @abstractmethod
    async def get_run(self, run_id: str) -> BacktestRun | None:
        ...
    
    
    @abstractmethod
    async def save_result(self, result: BacktestResult) -> BacktestResult:
        ...
    
    
    @abstractmethod
    async def get_results_by_run(self, run_id: str) -> list[BacktestResult]:
        ...
    
    
    @abstractmethod
    async def list_runs_by_strategy(self, strategy_id: str) -> list[BacktestRun]:
        ...


class EventLogRepository(ABC):
    """Repositorio para logs de eventos."""
    
    @abstractmethod
    async def save_event(
        self,
        event_type: str,
        source: str,
        symbol: str | None,
        details: dict[str, object],
    ) -> None:
        ...
    
    
    @abstractmethod
    async def list_events(
        self,
        event_type: str | None = None,
        source: str | None = None,
        symbol: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        ...
"""Testes unitarios para modelos de dominio."""

from saet.core.domain.enums import (
    Environment,
    OrderStatus,
    OrderType,
    PositionStatus,
    SignalType,
    StrategyStatus,
    Timeframe,
)
from saet.core.domain.models.account import Account, RiskConfig
from saet.core.domain.models.backtest import BacktestResult, BacktestRun
from saet.core.domain.models.market import Candle
from saet.core.domain.models.order import Order
from saet.core.domain.models.position import Position
from saet.core.domain.models.trading_signal import Signal
from saet.core.domain.models.strategy import Strategy, StrategyVersion


class TestEnums:
    def test_environment_values(self) -> None:
        assert Environment.BACKTEST.value == "backtest"
        assert Environment.DEMO.value == "demo"
        assert Environment.REAL.value == "real"

    def test_signal_type_values(self) -> None:
        assert SignalType.BUY.value == "buy"
        assert SignalType.SELL.value == "sell"
        assert SignalType.HOLD.value == "hold"
        assert SignalType.CLOSE.value == "close"

    def test_order_status_values(self) -> None:
        assert OrderStatus.PENDING.value == "pending"
        assert OrderStatus.FILLED.value == "filled"

    def test_timeframe_values(self) -> None:
        assert Timeframe.M5.value == "5m"
        assert Timeframe.H1.value == "1h"
        assert Timeframe.D1.value == "1d"


class TestStrategy:
    def test_create_strategy(self) -> None:
        strategy = Strategy(
            name="Test Strategy",
            description="A test strategy",
            module_path="strategies.test",
            timeframe=Timeframe.M5,
            symbols=["AAPL", "MSFT"],
        )
        assert strategy.name == "Test Strategy"
        assert strategy.timeframe == Timeframe.M5
        assert len(strategy.symbols) == 2
        assert strategy.id  # UUID gerado

    def test_strategy_not_validated_by_default(self) -> None:
        strategy = Strategy(name="Test")
        assert not strategy.is_validated()

    def test_strategy_is_validated(self) -> None:
        strategy = Strategy(
            name="Test",
            status_per_env={Environment.REAL: StrategyStatus.VALIDATED},
        )
        assert strategy.is_validated()

    def test_strategy_is_active_in_environment(self) -> None:
        strategy = Strategy(
            name="Test",
            status_per_env={
                Environment.DEMO: StrategyStatus.ACTIVE,
                Environment.REAL: StrategyStatus.INACTIVE,
            },
        )
        assert strategy.is_active_in(Environment.DEMO)
        assert not strategy.is_active_in(Environment.REAL)
        assert not strategy.is_active_in(Environment.BACKTEST)

    def test_validated_strategy_is_active(self) -> None:
        strategy = Strategy(
            name="Test",
            status_per_env={Environment.REAL: StrategyStatus.VALIDATED},
        )
        assert strategy.is_active_in(Environment.REAL)


class TestAccount:
    def test_create_account(self) -> None:
        account = Account(
            name="Demo Account",
            broker="TestBroker",
            server="demo.server.com",
            login="12345",
            environment=Environment.DEMO,
        )
        assert account.name == "Demo Account"
        assert account.environment == Environment.DEMO
        assert not account.is_connected

    def test_risk_config(self) -> None:
        config = RiskConfig(
            account_id="test-account",
            max_exposure=100000.0,
            max_daily_loss=5000.0,
            max_position_size=10000.0,
        )
        assert config.max_exposure == 100000.0
        assert config.max_daily_loss == 5000.0


class TestSignal:
    def test_create_signal(self) -> None:
        signal = Signal(
            strategy_id="strat-1",
            symbol="AAPL",
            signal_type=SignalType.BUY,
            price=150.0,
            volume=10.0,
        )
        assert signal.signal_type == SignalType.BUY
        assert signal.price == 150.0


class TestOrder:
    def test_create_order(self) -> None:
        order = Order(
            signal_id="sig-1",
            symbol="AAPL",
            order_type=OrderType.MARKET_BUY,
            volume=10.0,
            price=150.0,
        )
        assert order.status == OrderStatus.PENDING
        assert order.order_type == OrderType.MARKET_BUY


class TestPosition:
    def test_create_position(self) -> None:
        position = Position(
            symbol="AAPL",
            strategy_id="strat-1",
            account_id="acc-1",
            entry_price=150.0,
            volume=10.0,
        )
        assert position.status == PositionStatus.OPEN
        assert position.pnl == 0.0


class TestCandle:
    def test_create_candle(self) -> None:
        from datetime import datetime
        candle = Candle(
            symbol="AAPL",
            timestamp=datetime(2026, 1, 1, 10, 0),
            open=150.0,
            high=152.0,
            low=149.0,
            close=151.0,
            volume=1000000.0,
        )
        assert candle.symbol == "AAPL"
        assert candle.close == 151.0


class TestBacktest:
    def test_create_backtest_run(self) -> None:
        run = BacktestRun(
            strategy_id="strat-1",
            symbol="AAPL",
            parameters={"fast_period": 9},
        )
        assert run.strategy_id == "strat-1"

    def test_create_backtest_result(self) -> None:
        result = BacktestResult(
            run_id="run-1",
            total_trades=100,
            winning_trades=60,
            total_return=5000.0,
            win_rate=0.6,
        )
        assert result.total_trades == 100
        assert not result.validated


class TestStrategyVersion:
    def test_create_version(self) -> None:
        version = StrategyVersion(
            strategy_id="strat-1",
            version=1,
            parameters={"fast_period": 9},
            author="trader",
            changelog="Versao inicial",
        )
        assert version.version == 1
        assert version.author == "trader"
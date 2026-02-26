"""Testes unitarios para excecoes de dominio."""

from saet.core.domain.exceptions import (
    AssetLockError,
    BacktestError,
    EnvironmentNotConfiguredError,
    OrderExecutionError,
    RiskLimitExceededError,
    SAETError,
    StrategyNotFoundError,
    StrategyNotValidatedError,
)


class TestExceptions:
    def test_saet_error_is_base(self) -> None:
        error = SAETError("test error")
        assert isinstance(error, Exception)
        assert str(error) == "test error"

    def test_strategy_not_validated_error(self) -> None:
        error = StrategyNotValidatedError("SMA Crossover")
        assert "SMA Crossover" in str(error)
        assert "validada" in str(error)
        assert error.strategy_name == "SMA Crossover"

    def test_asset_lock_error(self) -> None:
        error = AssetLockError("AAPL", "strategy-1")
        assert "AAPL" in str(error)
        assert "strategy-1" in str(error)
        assert error.symbol == "AAPL"

    def test_risk_limit_exceeded_error(self) -> None:
        error = RiskLimitExceededError("max_exposure", 150000.0, 100000.0)
        assert "max_exposure" in str(error)
        assert error.current_value == 150000.0
        assert error.max_value == 100000.0

    def test_environment_not_configured_error(self) -> None:
        error = EnvironmentNotConfiguredError()
        assert "ambiente" in str(error).lower()

    def test_strategy_not_found_error(self) -> None:
        error = StrategyNotFoundError("abc-123")
        assert "abc-123" in str(error)
        assert error.strategy_id == "abc-123"

    def test_backtest_error(self) -> None:
        error = BacktestError("backtest failed")
        assert isinstance(error, SAETError)

    def test_order_execution_error(self) -> None:
        error = OrderExecutionError("order failed")
        assert isinstance(error, SAETError)
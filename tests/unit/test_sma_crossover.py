"""Testes unitarios para a estrategia SMA Crossover."""

from datetime import datetime, timedelta
from saet.core.domain.enums import SignalType
from saet.core.domain.models.market import Candle
from saet.strategies.examples.sma_crossover import SMACrossoverStrategy


class TestSMACrossoverStrategy:
    def test_strategy_name(self) -> None:
        strategy = SMACrossoverStrategy()
        assert strategy.name == "SMA Crossover"

    def test_strategy_description(self) -> None:
        strategy = SMACrossoverStrategy()
        assert "media" in strategy.description.lower() or "movel" in strategy.description.lower()

    def test_default_parameters(self) -> None:
        strategy = SMACrossoverStrategy()
        params = strategy.get_parameters()
        assert params["fast_period"] == 9
        assert params["slow_period"] == 21
        assert params["volume"] == 1.0

    def test_custom_parameters(self) -> None:
        strategy = SMACrossoverStrategy({"fast_period": 5, "slow_period": 10, "volume": 2.0})
        params = strategy.get_parameters()
        assert params["fast_period"] == 5
        assert params["slow_period"] == 10

    def test_hold_signal_with_insufficient_data(self) -> None:
        strategy = SMACrossoverStrategy({"fast_period": 3, "slow_period": 5, "volume": 1.0})
        candle = Candle(
            symbol="AAPL",
            timestamp=datetime(2026, 1, 1, 10, 0),
            open=150.0,
            high=152.0,
            low=149.0,
            close=151.0,
            volume=1000000.0,
        )
        signal = strategy.on_candle(candle, None)
        assert signal.signal_type == SignalType.HOLD

    def test_generates_signals_with_enough_data(self) -> None:
        strategy = SMACrossoverStrategy({"fast_period": 3, "slow_period": 5, "volume": 1.0})
        # Gerar dados suficientes para calcular medias
        base_time = datetime(2026, 1, 1, 10, 0)
        signals = []
        # Precos descendentes seguidos de ascendentes para forcar cruzamento
        prices = [100, 99, 98, 97, 96, 95, 96, 98, 100, 103]
        for i, price in enumerate(prices):
            candle = Candle(
                symbol="AAPL",
                timestamp=base_time + timedelta(minutes=5 * i),
                open=float(price) - 0.5,
                high=float(price) + 1.0,
                low=float(price) - 1.0,
                close=float(price),
                volume=1000000.0,
            )
            signal = strategy.on_candle(candle, None)
            signals.append(signal)
        # Deve ter pelo menos sinais HOLD no inicio (dados insuficientes)
        assert signals[0].signal_type == SignalType.HOLD

    def test_set_parameters(self) -> None:
        strategy = SMACrossoverStrategy()
        strategy.set_parameters({"fast_period": 15, "slow_period": 30, "volume": 5.0})
        params = strategy.get_parameters()
        assert params["fast_period"] == 15
        assert params["slow_period"] == 30

    def test_calculate_sma(self) -> None:
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        sma = SMACrossoverStrategy._calculate_sma(prices, 3, 0)
        assert sma == 40.0  # (30 + 40 + 50) / 3

    def test_calculate_sma_with_offset(self) -> None:
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        sma = SMACrossoverStrategy._calculate_sma(prices, 3, 1)
        assert sma == 30.0  # (20 + 30 + 40) / 3
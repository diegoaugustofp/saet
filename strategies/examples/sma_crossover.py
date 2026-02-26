"""Estrategia de exemplo: Cruzamento de Medias Moveis Simples (SMA Crossover).

Estrategia classica que gera sinal de compra quando a media rapida
cruza acima da media lenta, e venda no cruzamento inverso.

Esta estrategia serve como referencia para implementacao de novas estrategias.
"""


from typing import Any
from saet.core.domain.enums import SignalType
from saet.core.domain.models.market import Candle
from saet.core.domain.models.position import Position
from saet.core.domain.models.trading_signal import Signal
from saet.strategies.base import StrategyBase


class SMACrossoverStrategy(StrategyBase):
    """Estrategia de cruzamento de medias moveis simples."""

    def __init__(self, parameters: dict[str, Any] | None = None) -> None:
        default_params: dict[str, Any] = {
            "fast_period": 9,
            "slow_period": 21,
            "volume": 1.0,
        }
        if parameters:
            default_params.update(parameters)
        super().__init__(default_params)
        self._price_history: list[float] = []

    @property
    def name(self) -> str:
        return "SMA Crossover"

    @property
    def description(self) -> str:
        return (
            "Estrategia de cruzamento de medias moveis simples. "
            "Compra quando SMA rapida cruza acima da SMA lenta, "
            "vende no cruzamento inverso."
        )

    def on_candle(self, candle: Candle, position: Position | None) -> Signal:
        """Executa logica de cruzamento de medias moveis."""
        self._price_history.append(candle.close)

        fast_period = int(self._parameters.get("fast_period", 9))
        slow_period = int(self._parameters.get("slow_period", 21))
        volume = float(self._parameters.get("volume", 1.0))

        # Precisamos de dados suficientes para calcular ambas as medias
        if len(self._price_history) < slow_period + 1:
            return Signal(
                symbol=candle.symbol,
                signal_type=SignalType.HOLD,
                price=candle.close,
            )

        # Calcular medias moveis
        fast_sma_current = self._calculate_sma(self._price_history, fast_period, 0)
        fast_sma_previous = self._calculate_sma(self._price_history, fast_period, 1)
        slow_sma_current = self._calculate_sma(self._price_history, slow_period, 0)
        slow_sma_previous = self._calculate_sma(self._price_history, slow_period, 1)

        # Detectar cruzamento
        if fast_sma_previous <= slow_sma_previous and fast_sma_current > slow_sma_current:
            # Cruzamento para cima -> Sinal de compra
            if position is None:
                return Signal(
                    symbol=candle.symbol,
                    signal_type=SignalType.BUY,
                    price=candle.close,
                    volume=volume,
                )

        elif fast_sma_previous >= slow_sma_previous and fast_sma_current < slow_sma_current:
            # Cruzamento para baixo -> Sinal de venda/fechamento
            if position is not None:
                return Signal(
                    symbol=candle.symbol,
                    signal_type=SignalType.CLOSE,
                    price=candle.close,
                    volume=volume,
                )

        return Signal(
            symbol=candle.symbol,
            signal_type=SignalType.HOLD,
            price=candle.close,
        )

    @staticmethod
    def _calculate_sma(prices: list[float], period: int, offset: int = 0) -> float:
        """Calcula SMA para um periodo e offset dados.

        Args:
            prices: Lista de precos historicos.
            period: Periodo da media movel.
            offset: Deslocamento a partir do final (0 = mais recente).

        Returns:
            Valor da media movel simples.
        """
        end_idx = len(prices) - offset
        start_idx = end_idx - period
        if start_idx < 0:
            start_idx = 0
        window = prices[start_idx:end_idx]
        return sum(window) / len(window) if window else 0.0
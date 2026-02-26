"""Configuracao de fixtures para testes do SAET."""

import pytest


@pytest.fixture
def sample_strategy_params() -> dict[str, object]:
    """Parametros de exemplo para uma estrategia."""
    return {
        "fast_period": 9,
        "slow_period": 21,
        "volume": 1.0,
    }
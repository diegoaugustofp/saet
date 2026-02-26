"""Modelo de dominio: Strategy e StrategyVersion."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4
from saet.core.domain.enums import Environment, StrategyStatus, Timeframe


@dataclass
class StrategyVersion:
    """Versao de uma estrategia, registrando historico de alteracoes."""

    id: str = field(default_factory=lambda: str(uuid4()))
    strategy_id: str = ""
    version: int = 1
    parameters: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    author: str = ""
    changelog: str = ""


@dataclass
class Strategy:
    """Estrategia de trading."""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    module_path: str = ""
    current_version: int = 1
    parameters: dict[str, Any] = field(default_factory=dict)
    timeframe: Timeframe = Timeframe.M5
    symbols: list[str] = field(default_factory=list)
    status_per_env: dict[Environment, StrategyStatus] = field(default_factory=dict)
    versions: list[StrategyVersion] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


    def is_validated(self) -> bool:
        """Verifica se a estrategia esta validada para conta real."""
        return self.status_per_env.get(Environment.REAL) == StrategyStatus.VALIDATED


    def is_active_in(self, environment: Environment) -> bool:
        """Verifica se a estrategia esta ativa em um ambiente."""
        status = self.status_per_env.get(environment)
        return status in (StrategyStatus.ACTIVE, StrategyStatus.VALIDATED)
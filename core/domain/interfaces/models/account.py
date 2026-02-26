"""Modelo de dominio: Account e RiskConfig."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from saet.core.domain.enums import Environment


@dataclass
class RiskConfig:
    """Configuracao de limites de risco por conta."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    account_id: str = ""
    max_exposure: float = 0.0
    max_daily_loss: float = 0.0
    max_position_size: float = 0.0
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Account:
    """Conta de trading (demo ou real)."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    broker: str = ""
    server: str = ""
    login: str = ""
    encrypted_password: str = ""
    environment: Environment = Environment.DEMO
    risk_config: RiskConfig | None = None
    is_connected: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
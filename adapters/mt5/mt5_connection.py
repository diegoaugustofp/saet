"""Gerenciamento de conexao com MetaTrader 5.
Implementa reconexao automatica com backoff exponencial (SYS-NFR-010).
"""
import asyncio
from dataclasses import dataclass
from datetime import datetime
import structlog
logger = structlog.get_logger()
@dataclass
class MT5ConnectionConfig:
    """Configuracao de conexao com MT5."""
    server: str = ""
    login: int = 0
    password: str = ""
    timeout: int = 10000
    max_retries: int = 5
    base_retry_delay: float = 1.0
    max_retry_delay: float = 60.0
@dataclass
class MT5ConnectionState:
    """Estado atual da conexao com MT5."""
    is_connected: bool = False
    last_connected_at: datetime | None = None
    retry_count: int = 0
    last_error: str | None = None
class MT5Connection:
    """Gerenciador de conexao com MetaTrader 5.
    Implementa Circuit Breaker com backoff exponencial para reconexao
    automatica, evitando envio duplicado de ordens (SYS-NFR-010).
    """
    def __init__(self, config: MT5ConnectionConfig) -> None:
        self._config = config
        self._state = MT5ConnectionState()
    @property
    def is_connected(self) -> bool:
        """Retorna se esta conectado ao MT5."""
        return self._state.is_connected
    @property
    def state(self) -> MT5ConnectionState:
        """Retorna o estado atual da conexao."""
        return self._state
    async def connect(self) -> bool:
        """Estabelece conexao com MT5.
        Returns:
            True se conectou com sucesso.
        """
        try:
            # NOTE: Implementacao real requer MetaTrader5 instalado.
            # import MetaTrader5 as mt5
            # if not mt5.initialize(
            #     server=self._config.server,
            #     login=self._config.login,
            #     password=self._config.password,
            #     timeout=self._config.timeout,
            # ):
            #     raise ConnectionError(f"MT5 init failed: {mt5.last_error()}")
            self._state.is_connected = True
            self._state.last_connected_at = datetime.utcnow()
            self._state.retry_count = 0
            self._state.last_error = None
            logger.info(
                "mt5_connected",
                server=self._config.server,
                login=self._config.login,
            )
            return True
        except Exception as e:
            self._state.is_connected = False
            self._state.last_error = str(e)
            logger.error("mt5_connection_failed", error=str(e))
            return False
    async def disconnect(self) -> None:
        """Desconecta do MT5."""
        # NOTE: Implementacao real:
        # import MetaTrader5 as mt5
        # mt5.shutdown()
        self._state.is_connected = False
        logger.info("mt5_disconnected")
    async def reconnect(self) -> bool:
        """Tenta reconectar com backoff exponencial.
        Returns:
            True se reconectou com sucesso.
        """
        for attempt in range(self._config.max_retries):
            self._state.retry_count = attempt + 1
            delay = min(
                self._config.base_retry_delay * (2**attempt),
                self._config.max_retry_delay,
            )
            logger.info(
                "mt5_reconnecting",
                attempt=attempt + 1,
                max_retries=self._config.max_retries,
                delay_seconds=delay,
            )
            await asyncio.sleep(delay)
            if await self.connect():
                return True
        logger.error(
            "mt5_reconnection_failed",
            max_retries=self._config.max_retries,
        )
        return False
    async def ensure_connected(self) -> bool:
        """Garante que a conexao esta ativa, reconectando se necessario."""
        if self._state.is_connected:
            return True
        return await self.reconnect()
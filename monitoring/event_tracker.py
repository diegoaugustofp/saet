"""Rastreamento de eventos do SAET.

Responsavel por registrar eventos de conexao, sinais, ordens e erros
de forma estruturada para auditabilidade.

Requisitos: SYS-FR-050, SYS-FR-051
"""


from datetime import datetime
import structlog
from saet.core.domain.interfaces.repositories import EventLogRepository


logger = structlog.get_logger()


class EventTracker:
    """Rastreador de eventos do sistema.

    Registra eventos em log estruturado e, opcionalmente,
    persiste no banco de dados para consulta posterior.
    """

    def __init__(self, event_repository: EventLogRepository | None = None) -> None:
        self._repo = event_repository


    async def track(
        self,
        event_type: str,
        source: str,
        symbol: str | None = None,
        details: dict[str, object] | None = None,
    ) -> None:
        """Registra um evento.

        Args:
            event_type: Tipo do evento (connection, signal, order, error, etc).
            source: Origem do evento (strategy_name, mt5, scheduler, etc).
            symbol: Ativo relacionado, se aplicavel.
            details: Detalhes adicionais do evento.
        """

        event_details = details or {}

        # Log estruturado
        logger.info(
            "event_tracked",
            event_type=event_type,
            source=source,
            symbol=symbol,
            **{k: v for k, v in event_details.items() if isinstance(k, str)},
        )

        # Persistir no banco, se disponivel
        if self._repo is not None:
            await self._repo.save_event(
                event_type=event_type,
                source=source,
                symbol=symbol,
                details=event_details,
            )


    async def track_connection(
        self, status: str, server: str, error: str | None = None
    ) -> None:
        """Registra evento de conexao MT5."""

        await self.track(
            event_type="connection",
            source="mt5",
            details={"status": status, "server": server, "error": error},
        )


    async def track_signal(
        self,
        strategy_id: str,
        symbol: str,
        signal_type: str,
        price: float,
    ) -> None:
        """Registra evento de geracao de sinal."""

        await self.track(
            event_type="signal",
            source=strategy_id,
            symbol=symbol,
            details={"signal_type": signal_type, "price": price},
        )


    async def track_order(
        self,
        order_id: str,
        symbol: str,
        order_type: str,
        status: str,
        mt5_ticket: int | None = None,
    ) -> None:
        """Registra evento de envio/resposta de ordem."""

        await self.track(
            event_type="order",
            source="execution_engine",
            symbol=symbol,
            details={
                "order_id": order_id,
                "order_type": order_type,
                "status": status,
                "mt5_ticket": mt5_ticket,
            },
        )
    
    
    async def track_error(
        self, source: str, error: str, symbol: str | None = None
    ) -> None:
        """Registra evento de erro."""

        await self.track(
            event_type="error",
            source=source,
            symbol=symbol,
            details={"error": error, "timestamp": datetime.utcnow().isoformat()},
        )
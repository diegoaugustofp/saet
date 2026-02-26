"""Configuracao de logging estruturado com structlog.

Requisitos: SYS-FR-050, OBJ-04 (rastreabilidade e auditabilidade).
"""

import logging
import sys
import structlog


def setup_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """Configura logging estruturado para o SAET.

    Args:
        log_level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Formato de saida ('json' ou 'console').
    """

    # Configurar nivel de log
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Processadores compartilhados
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if log_format == "json":
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    # Configurar logging padrao do Python para bibliotecas externas
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=numeric_level,
    )
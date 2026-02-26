"""FastAPI application factory.

Ponto de entrada da API REST do SAET.
Requisito: SYS-NFR-040 (interface API na primeira versao).
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from saet.config.settings import get_settings
from saet.monitoring.logger import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Gerencia o ciclo de vida da aplicacao."""
    settings = get_settings()
    setup_logging(log_level=settings.log_level, log_format=settings.log_format)
    yield


def create_app() -> FastAPI:
    """Cria e configura a aplicacao FastAPI."""
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="SAET - Sistema de Automacao de Estrategias de Trading",
        lifespan=lifespan,
    )
    
    # Registrar rotas
    from saet.api.routes import (
        backtests,
        environments,
        execution,
        monitoring,
        performance,
        risk,
        strategies,
    )
    
    app.include_router(environments.router, prefix="/api/v1/environments", tags=["Ambientes"])
    app.include_router(strategies.router, prefix="/api/v1/strategies", tags=["Estrategias"])
    app.include_router(execution.router, prefix="/api/v1/execution", tags=["Execucao"])
    app.include_router(backtests.router, prefix="/api/v1/backtests", tags=["Backtests"])
    app.include_router(performance.router, prefix="/api/v1/performance", tags=["Performance"])
    app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["Monitoramento"])
    app.include_router(risk.router, prefix="/api/v1/risk", tags=["Risco"])
    
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "healthy", "version": settings.app_version}
    
    
    return app
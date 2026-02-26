"""Injecao de dependencias para a API FastAPI.

Centraliza a criacao e injecao de servicos e repositorios
nas rotas da API.
"""

# NOTE: Implementacao completa sera feita quando os repositorios
# SQLAlchemy estiverem implementados (proximo incremento).
#
# Exemplo de uso futuro:
#
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from saet.adapters.persistence.database import get_session
# from saet.adapters.persistence.sqlalchemy_repos import SQLAlchemyStrategyRepository
# from saet.core.services.strategy_service import StrategyService
#
#
# async def get_strategy_service(
#     session: AsyncSession = Depends(get_session),
# ) -> StrategyService:
#     repo = SQLAlchemyStrategyRepository(session)
#     return StrategyService(strategy_repository=repo)

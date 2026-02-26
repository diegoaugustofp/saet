"""Implementacao dos repositorios usando SQLAlchemy.
Implementacao concreta das interfaces definidas em core/domain/interfaces/repositories.py.
"""

# NOTE: Implementacao completa sera feita no proximo incremento (F1/F2).
# Este arquivo define o esqueleto dos repositorios SQLAlchemy.
# Cada metodo fara queries usando AsyncSession e mapeara os modelos
# SQLAlchemy (adapters/persistence/models.py) para entidades de dominio
# (core/domain/models/).
# Exemplo de implementacao futura:
#
# class SQLAlchemyStrategyRepository(StrategyRepository):
#     def __init__(self, session: AsyncSession) -> None:
#         self._session = session
#
#     async def save(self, strategy: Strategy) -> Strategy:
#         model = StrategyModel(
#             id=strategy.id,
#             name=strategy.name,
#             ...
#         )
#         self._session.add(model)
#         await self._session.flush()
#         return strategy
#
#     async def get_by_id(self, strategy_id: str) -> Strategy | None:
#         result = await self._session.get(StrategyModel, strategy_id)
#         if result is None:
#             return None
#         return Strategy(id=result.id, name=result.name, ...)
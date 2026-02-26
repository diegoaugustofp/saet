"""F2 - Servico de gestao de estrategias.

Responsavel por cadastrar, versionar, ativar e desativar estrategias,
com parametros configuraveis, selecao de ativo e logica de negociacao.

Requisitos: SYS-FR-010, SYS-FR-011, SYS-FR-012, SYS-FR-013
Caso de uso: UC-02
"""


from typing import Any
import structlog
from saet.core.domain.enums import Environment, StrategyStatus
from saet.core.domain.exceptions import StrategyNotFoundError, StrategyNotValidatedError
from saet.core.domain.interfaces.repositories import StrategyRepository
from saet.core.domain.models.strategy import Strategy, StrategyVersion


logger = structlog.get_logger()


class StrategyService:
    """Servico para gestao de estrategias de trading."""

    def __init__(self, strategy_repository: StrategyRepository) -> None:
        self._repo = strategy_repository


    async def create_strategy(
        self,
        name: str,
        description: str,
        module_path: str,
        parameters: dict[str, Any],
        timeframe: str,
        symbols: list[str],
        author: str = "",
    ) -> Strategy:
        """Cadastra uma nova estrategia.

        Args:
            name: Nome da estrategia.
            description: Descricao da estrategia.
            module_path: Caminho do modulo Python da estrategia.
            parameters: Parametros configuraveis.
            timeframe: Timeframe de operacao.
            symbols: Lista de ativos (tickers).
            author: Autor do cadastro.

        Returns:
            Estrategia criada com versao inicial.
        """

        from saet.core.domain.enums import Timeframe

        strategy = Strategy(
            name=name,
            description=description,
            module_path=module_path,
            parameters=parameters,
            timeframe=Timeframe(timeframe),
            symbols=symbols,
            status_per_env={
                Environment.BACKTEST: StrategyStatus.INACTIVE,
                Environment.DEMO: StrategyStatus.INACTIVE,
                Environment.REAL: StrategyStatus.INACTIVE,
            },
        )
    
        saved = await self._repo.save(strategy)
    
        version = StrategyVersion(
            strategy_id=saved.id,
            version=1,
            parameters=parameters,
            author=author,
            changelog="Versao inicial",
        )
    
        await self._repo.save_version(version)
    
        logger.info("strategy_created", strategy_id=saved.id, name=name)
    
        return saved
    
    
    async def update_strategy(
        self,
        strategy_id: str,
        parameters: dict[str, Any],
        author: str = "",
        changelog: str = "",
    ) -> Strategy:
        """Atualiza parametros de uma estrategia, criando nova versao.
    
        Args:
            strategy_id: ID da estrategia.
            parameters: Novos parametros.
            author: Autor da alteracao.
            changelog: Descricao da alteracao.
    
        Returns:
            Estrategia atualizada.
    
        """
    
        strategy = await self._repo.get_by_id(strategy_id)
        if strategy is None:
            raise StrategyNotFoundError(strategy_id)
        strategy.parameters = parameters
        strategy.current_version += 1
        saved = await self._repo.save(strategy)
        version = StrategyVersion(
            strategy_id=strategy_id,
            version=strategy.current_version,
            parameters=parameters,
            author=author,
            changelog=changelog,
        )
    
        await self._repo.save_version(version)
    
        logger.info(
            "strategy_updated",
            strategy_id=strategy_id,
            version=strategy.current_version,
        )
    
        return saved
    
    async def activate_strategy(
        self,
        strategy_id: str,
        environment: Environment,
    ) -> Strategy:
        """Ativa uma estrategia em um ambiente especifico.
    
        Args:
            strategy_id: ID da estrategia.
            environment: Ambiente de ativacao.
    
        Returns:
            Estrategia com status atualizado.
    
        Raises:
            StrategyNotValidatedError: Se tentar ativar em REAL sem validacao.
        """
    
        strategy = await self._repo.get_by_id(strategy_id)
    
        if strategy is None:
            raise StrategyNotFoundError(strategy_id)
    
        if environment == Environment.REAL and not strategy.is_validated():
            raise StrategyNotValidatedError(strategy.name)
    
        strategy.status_per_env[environment] = StrategyStatus.ACTIVE
    
        saved = await self._repo.save(strategy)
    
        logger.info(
            "strategy_activated",
            strategy_id=strategy_id,
            environment=environment.value,
        )
        return saved
    
    
    async def deactivate_strategy(
        self,
        strategy_id: str,
        environment: Environment,
    ) -> Strategy:
        """Desativa uma estrategia em um ambiente especifico."""
    
        strategy = await self._repo.get_by_id(strategy_id)
    
        if strategy is None:
            raise StrategyNotFoundError(strategy_id)
    
        strategy.status_per_env[environment] = StrategyStatus.INACTIVE
    
        saved = await self._repo.save(strategy)
    
        logger.info(
            "strategy_deactivated",
            strategy_id=strategy_id,
            environment=environment.value,
        )
    
        return saved
    
    
    async def list_strategies(self) -> list[Strategy]:
        """Lista todas as estrategias cadastradas."""
    
        return await self._repo.list_all()
    
    
    async def get_strategy(self, strategy_id: str) -> Strategy:
        """Retorna uma estrategia pelo ID."""
    
        strategy = await self._repo.get_by_id(strategy_id)
    
        if strategy is None:
            raise StrategyNotFoundError(strategy_id)
    
        return strategy
    
    
    async def get_versions(self, strategy_id: str) -> list[StrategyVersion]:
        """Retorna o historico de versoes de uma estrategia."""
    
        return await self._repo.get_versions(strategy_id)
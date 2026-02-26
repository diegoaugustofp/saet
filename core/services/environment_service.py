"""F1 - Servico de gestao de ambientes de execucao.

Responsavel por configurar e selecionar ambientes (backtest, demo, real),
conectar ao MT5 e aplicar regras de restricao para conta real.

Requisitos: SYS-FR-001, SYS-FR-002, SYS-FR-003
Caso de uso: UC-01
"""


import structlog
from saet.core.domain.enums import Environment
from saet.core.domain.exceptions import (
    EnvironmentNotConfiguredError,
    StrategyNotValidatedError,
)
from saet.core.domain.interfaces.repositories import AccountRepository, StrategyRepository
from saet.core.domain.models.account import Account


logger = structlog.get_logger()


class EnvironmentService:
    
    """Servico para gestao de ambientes de execucao."""
    def __init__(
        self,
        account_repository: AccountRepository,
        strategy_repository: StrategyRepository,
    ) -> None:
        self._account_repo = account_repository
        self._strategy_repo = strategy_repository
        self._active_account: Account | None = None
    
    
    @property
    def active_account(self) -> Account | None:
        
        """Retorna a conta ativa atual."""
        return self._active_account
    
    
    @property
    def active_environment(self) -> Environment:
        
        """Retorna o ambiente ativo atual."""
        if self._active_account is None:
            raise EnvironmentNotConfiguredError()
        return self._active_account.environment
    
    
    async def configure_account(self, account: Account) -> Account:
        """Configura e salva uma conta de trading.
        
        Args:
            account: Dados da conta a ser configurada.
        
        Returns:
            Conta salva com ID gerado.
        """
        saved = await self._account_repo.save(account)
        logger.info(
            "account_configured",
            account_id=saved.id,
            environment=saved.environment.value,
            broker=saved.broker,
        )
        return saved
    
    
    async def select_environment(self, account_id: str) -> Account:
        """Seleciona um ambiente de execucao ativando a conta correspondente.
        
        Args:
            account_id: ID da conta a ser ativada.
        
        Returns:
            Conta ativada.
        """
        account = await self._account_repo.get_by_id(account_id)
        if account is None:
            raise EnvironmentNotConfiguredError()
        self._active_account = account
        logger.info(
            "environment_selected",
            account_id=account.id,
            environment=account.environment.value,
        )
        return account
    
    
    async def validate_strategy_for_real(self, strategy_id: str) -> None:
        """Valida se uma estrategia pode ser executada em conta real.
        Args:
            strategy_id: ID da estrategia a ser validada.
        Raises:
            StrategyNotValidatedError: Se a estrategia nao esta validada.
        """
        strategy = await self._strategy_repo.get_by_id(strategy_id)
        if strategy is None or not strategy.is_validated():
            strategy_name = strategy.name if strategy else strategy_id
            raise StrategyNotValidatedError(strategy_name)
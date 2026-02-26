"""F7 - Servico de gestao de risco por conta.

Responsavel por configurar e aplicar limites de risco,
bloqueando abertura de posicoes que violem esses limites.

Requisitos: SYS-FR-060, SYS-NFR-050
Caso de uso: UC-07
"""


import structlog
from saet.core.domain.exceptions import RiskLimitExceededError
from saet.core.domain.interfaces.repositories import AccountRepository, PositionRepository
from saet.core.domain.models.account import RiskConfig


logger = structlog.get_logger()


class RiskService:
    """Servico de gestao de risco por conta."""

    def __init__(
        self,
        account_repository: AccountRepository,
        position_repository: PositionRepository,
    ) -> None:
        self._account_repo = account_repository
        self._position_repo = position_repository


    async def configure_risk(self, config: RiskConfig) -> RiskConfig:
        """Configura limites de risco para uma conta.

        Args:
            config: Configuracao de risco a ser salva.

        Returns:
            Configuracao salva.
        """

        saved = await self._account_repo.save_risk_config(config)
        logger.info(
            "risk_configured",
            account_id=config.account_id,
            max_exposure=config.max_exposure,
            max_daily_loss=config.max_daily_loss,
            max_position_size=config.max_position_size,
        )

        return saved


    async def get_risk_config(self, account_id: str) -> RiskConfig | None:
        """Retorna a configuracao de risco de uma conta."""

        return await self._account_repo.get_risk_config(account_id)


    async def validate_new_position(
        self,
        account_id: str,
        symbol: str,
        volume: float,
        price: float,
    ) -> None:
        """Valida se uma nova posicao respeita os limites de risco da conta.

        Args:
            account_id: ID da conta.
            symbol: Ativo da nova posicao.
            volume: Volume da nova posicao.
            price: Preco da nova posicao.

        Raises:
            RiskLimitExceededError: Se algum limite for violado.
        """

        config = await self._account_repo.get_risk_config(account_id)
        if config is None:
            return  # Sem limites configurados
        new_exposure = volume * price

        # Verificar tamanho maximo de posicao
        if config.max_position_size > 0 and new_exposure > config.max_position_size:
            raise RiskLimitExceededError(
                limit_type="max_position_size",
                current_value=new_exposure,
                max_value=config.max_position_size,
            )

        # Verificar exposicao total
        if config.max_exposure > 0:
            open_positions = await self._position_repo.list_open()
            total_exposure = sum(p.volume * p.current_price for p in open_positions)
            if total_exposure + new_exposure > config.max_exposure:
                raise RiskLimitExceededError(
                    limit_type="max_exposure",
                    current_value=total_exposure + new_exposure,
                    max_value=config.max_exposure,
                )

        logger.debug(
            "risk_validation_passed",
            account_id=account_id,
            symbol=symbol,
            new_exposure=new_exposure,
        )
"""F3 - Motor de execucao em tempo real.

Responsavel por executar estrategias periodicamente, gerar sinais
e enviar ordens ao broker.

Requisitos: SYS-FR-020, SYS-FR-021, SYS-FR-022, SYS-FR-025
Caso de uso: UC-03
"""

import structlog
from saet.core.domain.enums import Environment, OrderType, SignalType
from saet.core.domain.interfaces.broker_gateway import BrokerGateway
from saet.core.domain.interfaces.market_data import MarketDataProvider
from saet.core.domain.interfaces.repositories import (
    OrderRepository,
    PositionRepository,
    SignalRepository,
    StrategyRepository,
)
from saet.core.domain.interfaces.strategy_runner import StrategyRunner
from saet.core.domain.models.order import Order
from saet.core.domain.models.trading_signal import Signal
from saet.core.services.exclusivity_guard import ExclusivityGuard
from saet.core.services.risk_service import RiskService


logger = structlog.get_logger()


class ExecutionEngine:
    """Motor de execucao de estrategias em tempo real."""
    def __init__(
        self,
        broker_gateway: BrokerGateway,
        market_data: MarketDataProvider,
        strategy_repository: StrategyRepository,
        order_repository: OrderRepository,
        position_repository: PositionRepository,
        signal_repository: SignalRepository,
        exclusivity_guard: ExclusivityGuard,
        risk_service: RiskService,
        strategy_runners: dict[str, StrategyRunner] | None = None,
    ) -> None:
        self._broker = broker_gateway
        self._market_data = market_data
        self._strategy_repo = strategy_repository
        self._order_repo = order_repository
        self._position_repo = position_repository
        self._signal_repo = signal_repository
        self._exclusivity = exclusivity_guard
        self._risk = risk_service
        self._runners: dict[str, StrategyRunner] = strategy_runners or {}
    
    def register_runner(self, strategy_id: str, runner: StrategyRunner) -> None:
        """Registra um runner de estrategia."""
        self._runners[strategy_id] = runner
        logger.info("strategy_runner_registered", strategy_id=strategy_id, name=runner.name)
    
    
    async def run_cycle(self, environment: Environment, account_id: str) -> None:
        """Executa um ciclo completo de todas as estrategias ativas.
        
        Para cada ativo configurado:
        1. Verifica exclusividade (ExclusivityGuard)
        2. Obtem dados de mercado
        3. Executa logica da estrategia
        4. Valida risco
        5. Envia ordem ao broker
        6. Registra logs
        
        Args:
            environment: Ambiente de execucao atual.
            account_id: ID da conta ativa.
        """
        
        strategies = await self._strategy_repo.list_all()
        active_strategies = [s for s in strategies if s.is_active_in(environment)]
        logger.info(
            "execution_cycle_started",
            environment=environment.value,
            active_count=len(active_strategies),
        )
        for strategy in active_strategies:
            if environment == Environment.REAL and not strategy.is_validated():
                logger.warning(
                    "strategy_skipped_not_validated",
                    strategy_id=strategy.id,
                    name=strategy.name,
                )
                continue
            runner = self._runners.get(strategy.id)
            if runner is None:
                logger.warning(
                    "strategy_runner_not_found",
                    strategy_id=strategy.id,
                    name=strategy.name,
                )
                continue
            for symbol in strategy.symbols:
                await self._execute_strategy_for_symbol(
                    strategy_id=strategy.id,
                    runner=runner,
                    symbol=symbol,
                    timeframe=strategy.timeframe.value,
                    account_id=account_id,
                )
        logger.info("execution_cycle_completed", environment=environment.value)
    
    
    async def _execute_strategy_for_symbol(
        self,
        strategy_id: str,
        runner: StrategyRunner,
        symbol: str,
        timeframe: str,
        account_id: str,
    ) -> None:
        """Executa uma estrategia para um ativo especifico."""
        
        try:
            if not await self._exclusivity.can_execute(symbol, strategy_id):
                logger.debug(
                    "strategy_blocked_by_exclusivity",
                    strategy_id=strategy_id,
                    symbol=symbol,
                )
                return
            candle = await self._market_data.get_latest_candle(symbol, timeframe)
            position = await self._position_repo.get_open_by_symbol(symbol)
            signal = runner.on_candle(candle, position)
            signal.strategy_id = strategy_id
            signal.symbol = symbol
            await self._signal_repo.save(signal)
            if signal.signal_type == SignalType.HOLD:
                return
            if signal.signal_type in (SignalType.BUY, SignalType.SELL):
                await self._risk.validate_new_position(
                    account_id=account_id,
                    symbol=symbol,
                    volume=signal.volume,
                    price=signal.price,
                )
            order = self._create_order_from_signal(signal)
            await self._exclusivity.acquire_asset_lock(symbol, strategy_id)
            try:
                executed_order = await self._broker.send_order(order)
                await self._order_repo.save(executed_order)
                logger.info(
                    "order_executed",
                    strategy_id=strategy_id,
                    symbol=symbol,
                    signal=signal.signal_type.value,
                    status=executed_order.status.value,
                )
            finally:
                await self._exclusivity.release_asset_lock(symbol)
        except Exception:
            logger.exception(
                "strategy_execution_error",
                strategy_id=strategy_id,
                symbol=symbol,
            )
    
    
    @staticmethod
    def _create_order_from_signal(signal: Signal) -> Order:
        """Converte um sinal em uma ordem."""
        
        order_type_map = {
            SignalType.BUY: OrderType.MARKET_BUY,
            SignalType.SELL: OrderType.MARKET_SELL,
        }
        
        return Order(
            signal_id=signal.id,
            symbol=signal.symbol,
            order_type=order_type_map.get(signal.signal_type, OrderType.MARKET_BUY),
            volume=signal.volume,
            price=signal.price,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
        )
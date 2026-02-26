"""F3 - Guard de exclusividade por ativo.

Garante que apenas uma estrategia mantenha posicao aberta por ativo
e suspende execucao durante abertura de posicao.

Requisitos: SYS-FR-023, SYS-FR-024
"""

import asyncio
import structlog
from saet.core.domain.exceptions import AssetLockError
from saet.core.domain.interfaces.repositories import PositionRepository


logger = structlog.get_logger()


class ExclusivityGuard:
    """Gerencia exclusividade de posicao por ativo.
    
    Garante que:
    - Apenas uma estrategia tenha posicao aberta por ativo (SYS-FR-023).
    - Execucao e suspensa durante abertura de posicao (SYS-FR-024).
    """
    
    def __init__(self, position_repository: PositionRepository) -> None:
        self._position_repo = position_repository
        self._locks: dict[str, asyncio.Lock] = {}
        self._lock_holders: dict[str, str] = {}
    
    
    def _get_lock(self, symbol: str) -> asyncio.Lock:
        """Obtem ou cria lock para um ativo."""
        if symbol not in self._locks:
            self._locks[symbol] = asyncio.Lock()
        return self._locks[symbol]
    
    
    async def can_execute(self, symbol: str, strategy_id: str) -> bool:
        """Verifica se uma estrategia pode executar sobre um ativo.
        
        Retorna False se:
        - O ativo esta em processo de abertura de posicao (locked).
        - Outra estrategia ja tem posicao aberta no ativo.
        """
       
        lock = self._get_lock(symbol)
        if lock.locked():
            return False
        position = await self._position_repo.get_open_by_symbol(symbol)
        if position is not None and position.strategy_id != strategy_id:
            return False
        return True
    
    
    async def acquire_asset_lock(self, symbol: str, strategy_id: str) -> bool:
        """Adquire lock de exclusividade para um ativo.
        
        Args:
            symbol: Ativo a ser travado.
            strategy_id: ID da estrategia que esta adquirindo o lock.
        
        Returns:
            True se o lock foi adquirido com sucesso.
        
        Raises:
            AssetLockError: Se outra estrategia ja possui o lock.
        """
        
        lock = self._get_lock(symbol)
        if lock.locked() and self._lock_holders.get(symbol) != strategy_id:
            raise AssetLockError(symbol, self._lock_holders.get(symbol, "unknown"))
        await lock.acquire()
        self._lock_holders[symbol] = strategy_id
        logger.debug("asset_lock_acquired", symbol=symbol, strategy_id=strategy_id)
        return True
    
    
    async def release_asset_lock(self, symbol: str) -> None:
        """Libera lock de exclusividade de um ativo."""
        
        lock = self._get_lock(symbol)
        if lock.locked():
            lock.release()
            self._lock_holders.pop(symbol, None)
            logger.debug("asset_lock_released", symbol=symbol)
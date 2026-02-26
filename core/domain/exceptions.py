"""Excecoes do dominio SAET."""


class SAETError(Exception):
    """Excecao base do SAET."""


class BrokerConnectionError(SAETError):
    """Erro de conexao com o broker."""


class StrategyNotValidatedError(SAETError):
    """Tentativa de executar estrategia nao validada em conta real."""
    
    def __init__(self, strategy_name: str) -> None:
        self.strategy_name = strategy_name
        super().__init__(
            f"Estrategia '{strategy_name}' nao esta validada para execucao em conta real. "
            "Execute backtest e validacao em conta demo antes."
        )


class AssetLockError(SAETError):
    """Erro ao tentar adquirir lock de exclusividade por ativo."""
    
    def __init__(self, symbol: str, holding_strategy: str) -> None:
        self.symbol = symbol
        self.holding_strategy = holding_strategy
        super().__init__(
            f"Ativo '{symbol}' ja possui posicao aberta pela estrategia '{holding_strategy}'. "
            "Apenas uma estrategia pode manter posicao aberta por ativo."
        )


class RiskLimitExceededError(SAETError):
    """Violacao de limite de risco por conta."""
    
    def __init__(self, limit_type: str, current_value: float, max_value: float) -> None:
        self.limit_type = limit_type
        self.current_value = current_value
        self.max_value = max_value
        super().__init__(
            f"Limite de risco '{limit_type}' excedido: "
            f"valor atual={current_value}, maximo={max_value}."
        )


class EnvironmentNotConfiguredError(SAETError):
    """Ambiente de execucao nao configurado."""
    
    def __init__(self) -> None:
        super().__init__("Nenhum ambiente de execucao configurado. Configure um ambiente primeiro.")


class StrategyNotFoundError(SAETError):
    """Estrategia nao encontrada."""
    def __init__(self, strategy_id: str) -> None:
        self.strategy_id = strategy_id
        super().__init__(f"Estrategia com id '{strategy_id}' nao encontrada.")


class BacktestError(SAETError):
    """Erro durante execucao de backtest."""


class OrderExecutionError(SAETError):
    """Erro ao executar ordem no broker."""
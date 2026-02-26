# Documento de Decisoes de Arquitetura
## Sistema: SAET - Sistema de Automacao de Estrategias de Trading
## Versao: 1.0
## Data: 2026-02-26
## Status: Aprovado
---
# 1. Introducao
Este documento registra as decisoes de arquitetura tomadas para o projeto SAET, servindo como referencia para o time de desenvolvimento e para rastreabilidade das escolhas tecnicas.
---
# 2. Estilo Arquitetural
## 2.1 Decisao: Arquitetura Hexagonal (Ports & Adapters)
**Contexto:**
O requisito SYS-NFR-030 exige que a logica de estrategias seja desacoplada do nucleo de integracao com MT5. Alem disso, o sistema precisa operar em tres ambientes distintos (backtest, demo, real) com comportamentos diferentes para cada um.
**Decisao:**
Adotar a Arquitetura Hexagonal (Ports & Adapters), onde:
- O **dominio** (core) contem a logica de negocio pura, sem dependencias externas.
- **Ports** (interfaces abstratas) definem os contratos que o dominio espera.
- **Adapters** (implementacoes concretas) conectam o dominio ao mundo externo (MT5, banco de dados, API REST, CLI).
**Justificativa:**
- Estrategias podem ser adicionadas/modificadas sem alterar o modulo de integracao MT5.
- O mesmo motor de execucao serve para backtest, demo e real - basta trocar o adaptador.
- Facilita testes unitarios (mock de MT5 e banco de dados).
- Atende diretamente SYS-NFR-030.
**Consequencias:**
- Maior numero de arquivos e interfaces inicialmente.
- Curva de aprendizado para desenvolvedores nao familiarizados com o padrao.
- Flexibilidade e testabilidade significativamente maiores.
---
# 3. Stack Tecnologica
## 3.1 Linguagem: Python 3.11+
**Justificativa:** Requisito do projeto. Ecossistema maduro para trading quantitativo e integracao com MT5.
## 3.2 API REST: FastAPI
**Justificativa:** Framework async de alta performance, documentacao automatica (OpenAPI), validacao nativa com Pydantic. Atende SYS-NFR-040 (interface API na primeira versao).
## 3.3 CLI: Typer
**Justificativa:** CLI ergonomica baseada em type hints Python, complementa a API para operacoes administrativas. Atende SYS-NFR-040.
## 3.4 ORM e Banco de Dados: SQLAlchemy 2.0 + Alembic + PostgreSQL
**Justificativa:**
- SQLAlchemy 2.0: ORM robusto com suporte a async e tipagem moderna.
- Alembic: Migracoes versionadas e rastreavies.
- PostgreSQL para producao (confiabilidade, performance).
- SQLite para desenvolvimento e testes (simplicidade).
## 3.5 Integracao MT5: MetaTrader5 (pacote Python oficial)
**Justificativa:** SDK oficial da MetaQuotes para Python. Unica opcao suportada oficialmente.
## 3.6 Scheduler: APScheduler
**Justificativa:** Agendamento de tarefas em Python puro, sem necessidade de infraestrutura adicional (como Celery + Redis). Adequado para a escala inicial do SAET.
## 3.7 Validacao de Dados: Pydantic v2
**Justificativa:** Integracao nativa com FastAPI, validacao performatica, serializacao/deserializacao de modelos.
## 3.8 Logging: structlog
**Justificativa:** Logs estruturados em JSON, facilitando auditabilidade (OBJ-04) e integracao com ferramentas de monitoramento.
## 3.9 Seguranca de Credenciais: cryptography (Fernet)
**Justificativa:** Criptografia simetrica simples e segura para armazenamento de credenciais MT5 (SYS-NFR-020).
## 3.10 Testes: pytest + pytest-asyncio
**Justificativa:** Framework de testes padrao do ecossistema Python, com suporte a testes assincronos.
## 3.11 Gerenciamento de Dependencias: Poetry
**Justificativa:** Gerenciamento moderno de dependencias Python, com lock file para reprodutibilidade.
---
# 4. Estrutura de Modulos
```
saet/
|-- core/                           # Dominio puro (sem dependencias externas)
|   |-- domain/
|   |   |-- models/                 # Entidades de dominio
|   |   |-- enums.py                # Enumeracoes (Environment, SignalType, OrderStatus)
|   |   |-- interfaces/             # Ports (abstracoes)
|   |   |   |-- broker_gateway.py   # Interface para envio de ordens
|   |   |   |-- market_data.py      # Interface para dados de mercado
|   |   |   |-- strategy_runner.py  # Interface base para estrategias
|   |   |   |-- repositories.py     # Interfaces de persistencia
|   |   |-- exceptions.py           # Excecoes de dominio
|   |
|   |-- services/                   # Logica de negocio (use cases)
|       |-- environment_service.py  # F1: gestao de ambientes
|       |-- strategy_service.py     # F2: CRUD, versionamento, ativacao
|       |-- execution_engine.py     # F3: motor de execucao (sinais -> ordens)
|       |-- exclusivity_guard.py    # F3: exclusividade por ativo (SYS-FR-023/024)
|       |-- backtest_engine.py      # F4: motor de backtest
|       |-- performance_service.py  # F5: calculo de metricas e calibragem
|       |-- risk_service.py         # F7: validacao de limites de risco
|
|-- adapters/                       # Implementacoes concretas (adapters)
|   |-- mt5/
|   |   |-- mt5_broker_gateway.py   # Adapter: envio de ordens via MT5
|   |   |-- mt5_market_data.py      # Adapter: dados de mercado via MT5
|   |   |-- mt5_connection.py       # Gerenciamento de conexao/reconexao (SYS-NFR-010)
|   |
|   |-- persistence/
|   |   |-- sqlalchemy_repos.py     # Implementacao dos repositories
|   |   |-- database.py             # Setup do engine/session
|   |   |-- models.py               # Modelos SQLAlchemy (tabelas)
|   |   |-- migrations/             # Alembic migrations
|   |
|   |-- scheduler/
|   |   |-- apscheduler_adapter.py  # Scheduler para execucao periodica
|   |
|   |-- security/
|       |-- credential_vault.py     # Criptografia de credenciais (SYS-NFR-020)
|
|-- api/                            # Interface API REST (FastAPI)
|   |-- app.py                      # App factory
|   |-- dependencies.py             # Injecao de dependencias
|   |-- routes/
|   |   |-- environments.py         # Endpoints F1
|   |   |-- strategies.py           # Endpoints F2
|   |   |-- execution.py            # Endpoints F3 (start/stop)
|   |   |-- backtests.py            # Endpoints F4
|   |   |-- performance.py          # Endpoints F5
|   |   |-- monitoring.py           # Endpoints F6
|   |   |-- risk.py                 # Endpoints F7
|   |-- schemas/                    # Pydantic request/response schemas
|
|-- cli/                            # Interface CLI (Typer)
|   |-- commands/                   # Comandos espelhando as funcionalidades
|
|-- monitoring/                     # F6: Logging e monitoramento
|   |-- logger.py                   # Configuracao structlog
|   |-- event_tracker.py            # Rastreamento de eventos (SYS-FR-050)
|
|-- strategies/                     # Estrategias plugaveis
|   |-- base.py                     # Classe abstrata StrategyBase
|   |-- examples/                   # Estrategias exemplo
|
|-- config/
|   |-- settings.py                 # Configuracoes centralizadas (Pydantic Settings)
|
|-- tests/
    |-- unit/
    |-- integration/
    |-- conftest.py
```
---
# 5. Padroes de Design
## 5.1 Strategy Pattern (para estrategias de trading)
Cada estrategia de trading implementa a interface `StrategyBase`, definindo `on_candle()` e `get_parameters()`. Isso permite adicionar novas estrategias sem alterar o motor de execucao.
**Requisitos atendidos:** SYS-NFR-030, SYS-FR-010.
## 5.2 Repository Pattern (para persistencia)
Interfaces de repositorio definidas no dominio (`core/domain/interfaces/repositories.py`), com implementacoes concretas no adapter (`adapters/persistence/`). Permite trocar o banco de dados sem alterar a logica de negocio.
## 5.3 Guard Pattern (exclusividade por ativo)
`ExclusivityGuard` gerencia locks por ativo, garantindo que apenas uma estrategia mantenha posicao aberta por ativo (SYS-FR-023) e suspendendo execucoes durante abertura de posicao (SYS-FR-024).
## 5.4 Circuit Breaker (reconexao MT5)
Reconexao automatica com backoff exponencial ao MT5, evitando envio duplicado de ordens (SYS-NFR-010).
## 5.5 Dependency Injection (injecao de dependencias)
FastAPI's `Depends()` para injecao de servicos e repositorios nas rotas. Permite trocar implementacoes (ex: backtest vs. live) sem alterar a logica.
---
# 6. Separacao de Ambientes
O ambiente de execucao (BACKTEST, DEMO, REAL) determina quais adaptadores sao injetados:
| Ambiente  | BrokerGateway              | MarketData              | Restricoes                     |
|-----------|----------------------------|-------------------------|--------------------------------|
| BACKTEST  | BacktestBrokerGateway      | HistoricalMarketData    | Nenhuma                        |
| DEMO      | MT5BrokerGateway (demo)    | MT5MarketData (live)    | Nenhuma                        |
| REAL      | MT5BrokerGateway (real)    | MT5MarketData (live)    | Apenas estrategias validadas   |
**Requisitos atendidos:** SYS-FR-001, SYS-FR-002, SYS-FR-003.
---
# 7. Modelo de Dados (entidades principais)
- **Account**: id, name, broker, server, login, encrypted_password, environment, risk_limits
- **Strategy**: id, name, description, version, module_path, parameters, timeframe, status_per_env
- **StrategyVersion**: id, strategy_id, version, parameters, created_at, author, changelog
- **Signal**: id, strategy_id, symbol, timestamp, signal_type, candle_data
- **Order**: id, signal_id, symbol, order_type, volume, price, status, mt5_ticket, response
- **Position**: id, symbol, strategy_id, account_id, entry_price, volume, stop_loss, status
- **BacktestRun**: id, strategy_id, parameters, period_start, period_end, symbol, created_at
- **BacktestResult**: id, run_id, metrics_json, validated, validated_by, validated_at
- **RiskConfig**: id, account_id, max_exposure, max_daily_loss, max_position_size
- **EventLog**: id, timestamp, event_type, source, symbol, details_json
---
# 8. Fluxo de Execucao em Tempo Real (F3)
```
[APScheduler: a cada 5min]
        |
        v
[ExecutionEngine.run_cycle()]
        |
        |-- Para cada ativo configurado:
        |   |-- ExclusivityGuard.check(ativo)
        |   |-- MarketData.get_latest_candle(ativo)
        |   |-- Strategy.on_candle(candle, posicao_atual)
        |   |-- RiskService.validate(sinal, conta)
        |   |-- BrokerGateway.send_order(ordem)
        |   |-- EventTracker.log(sinal, ordem, resultado)
        |
        v
[Logs + DB persistidos]
```
**Requisitos atendidos:** SYS-FR-020, SYS-FR-021, SYS-FR-022, SYS-FR-023, SYS-FR-024, SYS-FR-025, SYS-NFR-001.
---
# 9. Implantacao (Deploy)
Para a v1, Docker Compose com tres servicos:
- **saet-app**: FastAPI + Scheduler + CLI
- **db**: PostgreSQL 16
- **mt5**: Container com MT5 (Wine + MT5 terminal)
O container MT5 e necessario porque o SDK Python do MT5 requer uma instancia do terminal em execucao (conforme requisito do ambiente operacional, secao 2.3 do SyRS).
---
# 10. Prioridade de Implementacao dos Epicos
1. **F1** - Gestao de ambientes de execucao (base para todos os outros)
2. **F2** - Gestao de estrategias (necessario para execucao)
3. **F3** - Execucao em tempo real (funcionalidade core)
4. **F7** - Gestao de risco por conta (seguranca antes de ir para real)
5. **F4** - Backtest e simulacao (validacao de estrategias)
6. **F5** - Analise de performance e calibragem (otimizacao)
7. **F6** - Monitoramento e logging (observabilidade)
---
# 11. Historico de Decisoes
| Data       | Decisao                                      | Justificativa                                    |
|------------|----------------------------------------------|--------------------------------------------------|
| 2026-02-26 | Arquitetura Hexagonal                        | Desacoplamento (SYS-NFR-030), testabilidade      |
| 2026-02-26 | FastAPI + Typer (API/CLI)                    | SYS-NFR-040, performance async                   |
| 2026-02-26 | SQLAlchemy 2.0 + PostgreSQL                  | Robustez, migracoes versionadas                  |
| 2026-02-26 | APScheduler                                  | Simplicidade, sem infra adicional                |
| 2026-02-26 | structlog                                    | Auditabilidade (OBJ-04), logs estruturados       |
| 2026-02-26 | Poetry                                       | Gerenciamento moderno de deps                    |
| 2026-02-26 | Strategy Pattern para estrategias de trading | SYS-NFR-030, extensibilidade                     |
| 2026-02-26 | Repository Pattern                           | Desacoplamento de persistencia                   |
| 2026-02-26 | Docker Compose para deploy                   | Ambiente operacional com MT5                     |

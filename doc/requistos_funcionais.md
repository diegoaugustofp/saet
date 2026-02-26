# System Requirements Specification (SyRS)
## System: SAET – Sistema de Automação de Estratégias de Trading
## Versão: 1.0
## Data: 2026-02-25
## Status: Draft

---

# 1. Introdução

## 1.1 Propósito do sistema
O propósito do SAET é automatizar a execução, validação e monitoramento de estratégias de trading em ativos do mercado americano, utilizando MetaTrader 5 (MT5) e Python, garantindo que apenas estratégias validadas atuem em conta real e que a performance possa ser medida e calibrada continuamente.

## 1.2 Propósito deste documento
Este SyRS descreve os requisitos de sistema do SAET em um formato adequado a projetos ágeis:
- Fornece uma visão de alto nível de objetivos e funcionalidades.
- Especifica requisitos de sistema testáveis em nível suficiente para guiar o backlog (épicos, features, histórias) e os critérios de aceitação.
- Suporta rastreabilidade entre objetivos de negócio, funcionalidades, requisitos e cenários de uso.

## 1.3 Escopo do sistema
O SAET abrange:
- Integração com MT5 para contas demo e reais.
- Execução automatizada de estratégias em múltiplos ativos e timeframes.
- Backtests e simulações para validação de estratégias.
- Cálculo de métricas de performance e apoio à calibragem.
- Monitoramento e logging da execução.

Fora de escopo:
- Interface gráfica avançada de trading manual.
- Execução em outras plataformas que não MT5.
- Otimização automática sofisticada além de grids de parâmetros configuráveis.

## 1.4 Definições, acrônimos e abreviações
- SAET: Sistema de Automação de Estratégias de Trading.
- MT5: MetaTrader 5.
- Conta demo: Conta de simulação em MT5.
- Conta real: Conta com capital real em MT5.
- Estratégia: Conjunto de regras de entrada, saída e gestão de risco.
- Backtest: Execução retrospectiva de uma estratégia em dados históricos.
- Scheduler: Componente responsável por disparar a execução periódica das estratégias.
- Métricas de performance: indicadores como retorno, drawdown, índice de Sharpe, taxa de acerto, payoff.

## 1.5 Stakeholders
- STK-01 Analista de Requisitos.
- STK-02 Trader Quantitativo / Estrategista.
- STK-03 Desenvolvedor Python.
- STK-04 Administrador da Conta MT5.
- STK-05 Gestor de Risco.
- STK-06 Administrador de Sistema / DevOps.

---

# 2. Visão geral do sistema

## 2.1 Perspectiva do produto
O SAET é um sistema de apoio ao trading quantitativo que se conecta a MT5 para execução de ordens, mantendo a lógica de estratégia, backtesting, métricas e monitoramento em sua própria camada de aplicação.

Componentes principais:
- Módulo de integração MT5.
- Módulo de gestão de estratégias.
- Módulo de execução em tempo real (live trading).
- Módulo de backtest.
- Módulo de análise de performance e calibragem.
- Módulo de monitoramento e logging.

## 2.2 Classes de usuários
- Trader Quantitativo: define estratégias, parâmetros, executa backtests e calibra estratégias.
- Gestor de Risco: analisa métricas e valida estratégias para uso em conta real.
- Administrador da Conta MT5: gerencia credenciais e ambientes.
- Administrador de Sistema: cuida de deploy, monitoramento técnico e infraestrutura.

## 2.3 Ambiente operacional

- Servidor de aplicação (ou container) executando o SAET.
- Sistema operacional Windows, uma vez que a plataforma MetaTrader 5 é nativa para esse ambiente e pode apresentar problemas de compatibilidade em outros sistemas.
- Instalação do MetaTrader 5 (terminal cliente) no mesmo host onde o SAET for executado, utilizando instalação padrão fornecida pela corretora ou pelo site oficial.
- API/SDK Python do MT5 instalada em ambiente compatível, incluindo a biblioteca `MetaTrader5` instalada via `pip install MetaTrader5`.
- Ambiente Python configurado com suporte à instalação de pacotes via `pip`, podendo ser:
  - Instalação direta do Python com a opção “Add Python to PATH” habilitada, ou
  - Ambiente Anaconda devidamente configurado.
- Bibliotecas auxiliares como `pandas` e `matplotlib` instaladas, quando necessárias para análise e visualização.
- Conexão à internet com os servidores MT5 do broker.
- Banco de dados para parâmetros, resultados e logs.
- No container ou host em que o SAET for executado, deve estar em execução uma instância do terminal MetaTrader 5 que permita o acesso à API de negociação.


## 2.4 Premissas e dependências
- Existência de conta(s) demo e real ativas em broker compatível com MT5.
- Disponibilidade da API MetaTrader5 para Python.
- Disponibilidade de dados históricos adequados para backtests.
- Time de desenvolvimento com conhecimento em Python e integração MT5.

---

# 3. Objetivos de negócio (épicos de produto)

- OBJ-01 – Automatizar a execução consistente de estratégias de trading em múltiplos ativos do mercado americano.
- OBJ-02 – Garantir que nenhuma estratégia opere em conta real sem validação prévia em backtest e conta demo.
- OBJ-03 – Disponibilizar métricas de performance confiáveis para permitir calibragem sistemática das estratégias.
- OBJ-04 – Assegurar rastreabilidade e auditabilidade das decisões de trading automatizadas.

Esses objetivos orientam a priorização de épicos e features no backlog.

---

# 4. Funcionalidades de alto nível (features / épicos)

Cada funcionalidade abaixo corresponde a um “épico” ou grande feature a ser decomposta em histórias de usuário.

## 4.1 F1 – Gestão de ambientes de execução
Permitir configurar e selecionar ambientes (backtest, conta demo, conta real), garantindo que restrições de segurança (especialmente conta real) sejam respeitadas.

## 4.2 F2 – Gestão de estratégias
Permitir cadastrar, versionar, ativar e desativar estratégias, com parâmetros configuráveis, seleção de ativo e lógica de negociação.

## 4.3 F3 – Execução em tempo real (live trading)
Executar estratégias ativas em tempo quase real, gerando sinais e enviando ordens para MT5, bem como gerindo posições e exclusividade por ativo.

## 4.4 F4 – Backtest e simulação
Executar backtests das estratégias em dados históricos com cenários variados e registrar resultados.

## 4.5 F5 – Análise de performance e calibragem
Calcular métricas, comparar calibrações de parâmetros e marcar combinações validadas para uso em conta real.

## 4.6 F6 – Monitoramento e logging
Registrar eventos relevantes e disponibilizar um painel de monitoramento para acompanhar execução e histórico.

## 4.7 F7 – Gestão de risco por conta
Configurar e aplicar limites de risco por conta, bloqueando aberturas de posições que violem esses limites.

---

# 5. Casos de uso de sistema (cenários-chave)

## 5.1 UC-01 – Gerir ambiente de execução

**Resumo:** Configurar e selecionar o ambiente (backtest/demo/real), conectando ao MT5 e aplicando regras de restrição para conta real.  
**Atores:** Trader Quantitativo, Administrador da Conta MT5.

Pré-condições:
- PRC-UC01-01: Usuário autenticado.
- PRC-UC01-02: SAET operacional.
- PRC-UC01-03: Credenciais MT5 disponíveis.

Fluxo principal:
1. Usuário abre a configuração de ambiente.
2. Seleciona tipo de ambiente (backtest, demo, real).
3. Informa servidor, login e senha.
4. SAET testa conexão com MT5.
5. SAET define ambiente como ativo.
6. SAET aplica regras de restrição para conta real (bloqueando estratégias não validadas).

Pós-condições:
- POC-UC01-01: Ambiente ativo registrado para a sessão.
- POC-UC01-02: Execução em conta real só possível para estratégias marcadas como validadas.

---

## 5.2 UC-02 – Gerir estratégias de trading

**Resumo:** Cadastrar, versionar, ativar/desativar estratégias, selecionar ativos e ajustar parâmetros.  
**Atores:** Trader Quantitativo, Desenvolvedor.

Fluxo principal (cadastro):
1. Usuário requisita cadastro de nova estratégia.
2. SAET apresenta formulário com campos obrigatórios.
3. Usuário preenche nome, descrição, tipo de ativo, timeframe e ativo(s) (ticker[s]).
4. Usuário define parâmetros configuráveis.
5. Usuário associa lógica (código ou módulo).
6. SAET valida e cria versão inicial da estratégia.

Fluxo de ativação/desativação:
1. Usuário lista estratégias.
2. Ajusta status por ambiente (backtest/demo/real).
3. SAET aplica regras de bloqueio para conta real se não validada.

---

## 5.3 UC-03 – Executar estratégias em tempo real

**Resumo:** Rodar estratégias periodicamente, gerar sinais e enviar ordens para MT5, garantindo exclusividade por ativo e gerenciamento segregado por ativo.  
**Atores:** Sistema (scheduler), Trader Quantitativo.

Fluxo principal:
1. Scheduler detecta novo tick/candle.
2. SAET obtém dados de mercado via MT5 para cada ativo configurado.
3. SAET executa lógica de cada estratégia ativa por ativo.
4. Estratégias retornam sinais.
5. SAET verifica se existe outra estratégia com posição aberta no mesmo ativo e aplica regra de exclusividade.
6. SAET converte sinais em ordens, aplica regras de risco e limites por conta.
7. SAET envia ordens a MT5.
8. SAET registra logs de sinais, ordens e respostas, separados por ativo.

---

## 5.4 UC-04 – Executar backtests

**Resumo:** Executar backtests de estratégias em dados históricos, em um ou mais cenários.  
**Atores:** Trader Quantitativo.

Fluxo principal:
1. Usuário seleciona “executar backtest”.
2. Seleciona estratégia(s), período histórico, ativos e grade de parâmetros.
3. Inicia o backtest.
4. SAET executa a estratégia nos dados históricos.
5. SAET calcula métricas por cenário.
6. SAET persiste resultados.

---

## 5.5 UC-05 – Analisar performance e calibrar

**Resumo:** Visualizar métricas, comparar calibrações e marcar combinações como validadas.  
**Atores:** Trader Quantitativo, Gestor de Risco.

Fluxo principal:
1. Usuário abre painel de análise de performance.
2. Filtra por estratégia, período, ambiente, ativo.
3. Visualiza métricas (retorno, drawdown, Sharpe, taxa de acerto etc.).
4. Seleciona calibrações para comparação lado a lado.
5. Marca combinações estratégia+parâmetros+período como “validadas”, conforme critérios.

---

## 5.6 UC-06 – Monitorar execução e logs

**Resumo:** Monitorar status de conexão, estratégias, posições e eventos.  
**Atores:** Trader Quantitativo, Administrador de Sistema.

Fluxo principal:
1. Usuário acessa painel de monitoramento.
2. Visualiza status de conexão, estratégias ativas, posições abertas por ativo, resultados agregados.
3. Aplica filtros de data, estratégia, ativo e tipo de evento.
4. Visualiza logs detalhados.

---

## 5.7 UC-07 – Configurar limites de risco por conta

**Resumo:** Definir limites de risco por conta e garantir que novas posições respeitem esses limites.  
**Atores:** Gestor de Risco, Trader Quantitativo.

Fluxo principal:
1. Usuário acessa a tela de configuração de risco por conta.
2. Define limites como exposição máxima total, perda máxima diária e tamanho máximo de posição por conta.
3. Salva as configurações.
4. SAET passa a aplicar esses limites em todas as solicitações de abertura de novas posições.

---

# 6. Requisitos de sistema (funcionais)

## 6.1 Gestão de ambientes (F1, UC-01)

**SYS-FR-001 – Seleção de ambiente**  
O sistema deve permitir ao usuário selecionar o ambiente de execução entre backtest, conta demo e conta real.

**SYS-FR-002 – Conexão com MT5**  
O sistema deve estabelecer e validar conexão com um servidor MT5, utilizando credenciais de conta demo ou real fornecidas pelo usuário.

**SYS-FR-003 – Restrição em conta real**  
O sistema deve impedir a execução em conta real de qualquer estratégia que não esteja marcada como validada.

---

## 6.2 Gestão de estratégias (F2, UC-02)

**SYS-FR-010 – Cadastro de estratégia**  
O sistema deve permitir o cadastro de estratégias com nome, descrição, tipo de ativo, timeframe, parâmetros configuráveis e lógica de negociação.

**SYS-FR-011 – Versionamento de estratégia**  
O sistema deve manter histórico de versões de cada estratégia, registrando data, autor e descrição de alterações relevantes.

**SYS-FR-012 – Ativação/desativação**  
O sistema deve permitir ativar e desativar estratégias por ambiente (backtest, demo, real).

**SYS-FR-013 – Seleção de ativo (ticker)**  
O sistema deve permitir que, para cada estratégia, seja selecionado o ativo (ticker) ou conjunto de ativos sobre os quais a estratégia será executada.

---

## 6.3 Execução em tempo real (F3, UC-03)

**SYS-FR-020 – Geração de sinais**  
O sistema deve executar periodicamente as estratégias ativas para gerar sinais de compra, venda, manutenção ou encerramento.

**SYS-FR-021 – Envio de ordens**  
O sistema deve enviar ordens ao MT5 com base nos sinais gerados, respeitando tipo de ordem, volume e regras de risco definidas.

**SYS-FR-022 – Gestão de posições**  
O sistema deve monitorar e ajustar posições abertas de acordo com as regras da estratégia, incluindo ajustes de stop e encerramento.

**SYS-FR-023 – Exclusividade de posição por ativo**  
O sistema deve impedir que mais de uma estratégia mantenha posições abertas simultaneamente no mesmo ativo em um mesmo ambiente de execução.

**SYS-FR-024 – Suspensão de estratégias durante abertura de posição**  
O sistema deve suspender temporariamente a execução das estratégias ativas sobre um ativo enquanto uma nova posição estiver em processo de abertura nesse mesmo ativo, retomando a execução após a conclusão ou falha da abertura da posição.

**SYS-FR-025 – Gerenciamento por ativo**  
O sistema deve realizar o gerenciamento de ordens, posições e sinais de forma segregada por ativo, garantindo que decisões e controles relativos a um ativo não afetem o tratamento de outros ativos.

---

## 6.4 Backtest e simulação (F4, UC-04)

**SYS-FR-030 – Execução de backtest**  
O sistema deve executar backtests de estratégias em dados históricos configurados pelo usuário.

**SYS-FR-031 – Cenários de teste**  
O sistema deve permitir definir cenários de backtest com diferentes períodos, ativos e grades de parâmetros.

**SYS-FR-032 – Registro de resultados de backtest**  
O sistema deve registrar resultados de cada cenário de backtest, incluindo métricas, parâmetros e versão da estratégia.

---

## 6.5 Análise de performance e calibragem (F5, UC-05)

**SYS-FR-040 – Cálculo de métricas**  
O sistema deve calcular métricas de performance como retorno, drawdown, índice de Sharpe, taxa de acerto e payoff médio por estratégia e período.

**SYS-FR-041 – Comparação de calibrações**  
O sistema deve permitir comparar, em uma única visualização, diferentes calibrações de parâmetros de uma mesma estratégia.

**SYS-FR-042 – Marcação de combinação validada**  
O sistema deve permitir marcar combinações estratégia+parâmetros+período como “validadas”, com base em critérios configuráveis.

---

## 6.6 Monitoramento e logging (F6, UC-06)

**SYS-FR-050 – Log de eventos**  
O sistema deve registrar em logs eventos de conexão, geração de sinais, envio de ordens, respostas do MT5 e erros.

**SYS-FR-051 – Painel de monitoramento**  
O sistema deve fornecer um painel que exiba status de conexão, estratégias ativas, posições abertas e resultados agregados por dia e por estratégia.

---

## 6.7 Gestão de risco por conta (F7, UC-07)

**SYS-FR-060 – Aplicação de limites de risco por conta**  
O sistema deve impedir a abertura de novas posições quando a aplicação dos limites de risco configurados para a conta resultar em violação dos limites de exposição ou perda máxima definidos para essa conta.

## 6.8 Integração técnica com MT5

**SYS-FR-070 – Inicialização da integração com MT5**  
O sistema deve inicializar a integração com o MetaTrader 5 antes de executar qualquer operação de leitura de dados de mercado ou envio de ordens, verificando o sucesso da inicialização e registrando em log o estado do terminal conectado.

**SYS-FR-071 – Verificação de terminal MT5**  
O sistema deve consultar e registrar informações do terminal MetaTrader 5 conectado (por exemplo, conta ativa, servidor, modo demo/real) no momento da inicialização da integração, de forma a validar que o ambiente selecionado no SAET é compatível com o terminal.

**SYS-FR-072 – Encerramento da integração com MT5**  
O sistema deve encerrar a integração com o MetaTrader 5 ao finalizar a execução planejada (por exemplo, término de sessão, parada do serviço ou fim de um lote de backtests), garantindo o fechamento adequado da sessão com o terminal.


---

# 7. Requisitos não funcionais

## 7.1 Desempenho

**SYS-NFR-001 – Latência de decisão**  
O sistema deve processar a geração de sinais e o envio de ordens em até um intervalo configurável adequado ao timeframe operado, sendo que, na primeira versão, o timeframe suportado será de 5 minutos e o sistema deve concluir o processamento em até 5 segundos após o fechamento de cada candle de 5 minutos.

**SYS-NFR-002 – Capacidade de backtest**  
O sistema deve suportar a execução de backtests com pelo menos N anos de dados em timeframe de 5 minutos para um ativo, concluindo o processamento em um tempo acordado (por exemplo, até 24 horas para o conjunto de cenários e grade de parâmetros definidos).

---

## 7.2 Confiabilidade e disponibilidade

**SYS-NFR-010 – Reconexão MT5**  
O sistema deve tentar reconectar automaticamente ao MT5 em caso de perda de conexão, conforme política configurável, evitando envio duplicado de ordens.

---

## 7.3 Segurança

**SYS-NFR-020 – Proteção de credenciais**  
O sistema deve armazenar credenciais de contas MT5 de forma protegida, com mecanismos de criptografia e controle de acesso.

**SYS-NFR-021 – Controle de acesso a conta real**  
O sistema deve exigir perfil de permissão apropriado para habilitar execução em conta real e registrar quem habilitou.

---

## 7.4 Manutenibilidade

**SYS-NFR-030 – Desacoplamento de estratégias**  
O sistema deve manter a lógica de estratégias desacoplada do núcleo de integração com MT5, permitindo adicionar ou modificar estratégias sem alterar o módulo de integração.

---

## 7.5 Interface e arquitetura

**SYS-NFR-040 – Interface API/CLI na primeira versão**  
Na primeira versão, o sistema deve expor suas funcionalidades por meio de interfaces de API e/ou CLI, sem exigir interface gráfica completa.

---

## 7.6 Restrições e parâmetros de risco

**SYS-NFR-050 – Limites iniciais de risco por conta**  
O sistema deve permitir configurar limites iniciais de risco por conta (por exemplo, exposição máxima total, perda máxima diária e tamanho máximo de posição por conta), devendo aplicar esses limites na validação de abertura de novas posições em qualquer estratégia associada à conta.

## 7.7 Desempenho

**SYS-NFR-003 – Dependência de terminal MT5 em execução**  
O sistema deve considerar como pré-requisito de operação que o terminal MetaTrader 5 esteja em execução no mesmo host do ambiente Python utilizado pelo SAET, uma vez que a biblioteca `MetaTrader5` depende de um terminal ativo para estabelecer a conexão.

**SYS-NFR-004 – Inicialização e encerramento de sessão MT5**  
O sistema deve utilizar chamadas equivalentes a `mt5.initialize()` para estabelecer a sessão com o terminal MetaTrader 5 antes de qualquer operação de mercado ou consulta de dados, e chamadas equivalentes a `mt5.shutdown()` para encerrar a sessão ao finalizar o processamento ou quando o módulo de integração for desligado.



---

# 8. Adaptação para projetos ágeis

## 8.1 Relação com backlog
- Cada funcionalidade (F1–F7) pode ser tratada como épico.
- Cada UC e conjunto de requisitos associados pode ser decomposto em histórias de usuário.
- Os IDs de requisito (SYS-FR-xxx, SYS-NFR-xxx) devem ser usados como referência em histórias, critérios de aceitação e testes automatizados.

## 8.2 Critérios de aceitação (exemplo)

Para SYS-FR-003 – Restrição em conta real:

- Given que uma estratégia não está marcada como validada  
- And que o ambiente selecionado é conta real  
- When o usuário tenta ativar a estratégia para conta real  
- Then o sistema deve bloquear a ativação  
- And exibir mensagem indicando que a estratégia precisa ser validada em backtest e conta demo.

---

# 9. Rastreabilidade (resumo)

| Objetivo | Funcionalidades (F) | Casos de Uso                | Requisitos de sistema                    |
|----------|---------------------|-----------------------------|------------------------------------------|
| OBJ-01   | F2, F3, F6          | UC-02, UC-03, UC-06         | SYS-FR-010, 011, 012, 020, 021, 022, 023, 024, 025, 050, 051 |
| OBJ-02   | F1, F2, F4, F5, F7  | UC-01, UC-02, UC-04, UC-05, UC-07 | SYS-FR-001, 002, 003, 030, 031, 032, 040, 041, 042, 060     |
| OBJ-03   | F4, F5              | UC-04, UC-05                | SYS-FR-030, 031, 032, 040, 041, 042; SYS-NFR-001, 002       |
| OBJ-04   | F1, F3, F4, F6      | UC-01, UC-03, UC-04, UC-06  | SYS-FR-002, 011, 032, 050, 051; SYS-NFR-020, 021, 030, 010  |

---

# 10. Questões em aberto (para próximos incrementos)

- Q01: Quais métricas exatas (fórmulas) serão adotadas como padrão para cada indicador de performance (Sharpe, drawdown, etc.)?

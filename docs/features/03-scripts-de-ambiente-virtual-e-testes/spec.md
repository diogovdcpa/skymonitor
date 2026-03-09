# Feature 03: Scripts de ambiente virtual e testes

- ID: `03`
- Slug: `scripts-de-ambiente-virtual-e-testes`
- Criada em: 2026-03-09
- Status geral: `concluida`
- Resumo: Adicionar a pasta env-script com scripts shell para iniciar o ambiente virtual, encerrar a sessao do ambiente e executar a suite de testes com o gate de venv do projeto.

## 1. Objetivo

Padronizar o uso do ambiente virtual do projeto com uma pasta `env-script/` contendo scripts simples e previsiveis para ativar o fluxo de desenvolvimento, encerrar a sessao atual do ambiente virtual e executar os testes usando o gate obrigatorio de `VIRTUAL_ENV`.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `README.md`, que hoje documenta ativacao manual da `.venv` e exemplos de execucao com o gate de ambiente virtual
  - `app.py`, CLI Python principal que depende de execucao manual em ambiente corretamente ativado
  - `requirements.txt`, base minima do ambiente Python atual
  - `docs/features/03-scripts-de-ambiente-virtual-e-testes/spec.md`
  - Nova pasta `env-script/` com scripts operacionais para desenvolvimento local
- Dependencias tecnicas:
  - Shell script compativel com o ambiente local do projeto
  - Ambiente virtual existente em `.venv/`
  - `pytest` como executor padrao para a suite de testes, mesmo que a pasta `tests/` ainda precise ser criada em entregas de codigo
- Riscos e restricoes:
  - "Encerrar o ambiente virtual" nao pode desligar a shell do usuario a partir de um processo filho comum; a implementacao precisa considerar `deactivate` via `source` ou deixar essa restricao explicitada
  - Scripts executados com `bash script.sh` nao persistem alteracoes de ambiente no shell chamador; isso afeta principalmente o script de ativacao
  - O repositorio ainda nao possui suite de testes implementada, entao o script de testes precisa falhar de forma clara ou ser acompanhado da criacao inicial da estrutura de testes
  - A pasta solicitada pelo usuario e `env-script`, logo a convencao deve ser mantida mesmo fugindo de nomes mais comuns como `scripts/`

## 3. Referencias externas (opcional, recomendado)

Nao aplicavel nesta etapa. A spec foi baseada no contexto local da codebase e nas regras operacionais documentadas em `AGENTS.md` e `README.md`.

## 4. Escopo

### Em escopo

- Criar a pasta `env-script/` na raiz do repositorio.
- Definir um script para preparar a sessao de desenvolvimento com ativacao da `.venv` e execucao do gate de `VIRTUAL_ENV`.
- Definir um script para encerrar o uso do ambiente virtual na sessao atual, respeitando as limitacoes de shell script.
- Definir um script para executar `pytest -q` com o gate obrigatorio de ambiente virtual.
- Atualizar a documentacao minima de uso para indicar como os scripts devem ser invocados.
- Cobrir os scripts com testes ou validacoes automatizadas compativeis com a abordagem adotada.

### Fora de escopo

- Alterar o comportamento funcional do CLI `app.py`.
- Introduzir empacotamento Python com `pyproject.toml`.
- Criar automacao de CI/CD.
- Reestruturar toda a organizacao de scripts utilitarios fora do necessario para `env-script/`.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: Definir a interface dos scripts e resolver a restricao tecnica de ativacao/desativacao do ambiente virtual em shell.
  - Entregaveis: Decisao sobre nomes dos scripts, forma de invocacao (`source` quando necessario) e comportamento esperado em caso de erro.
  - Criterio de conclusao: Fluxo operacional documentado e consistente com `AGENTS.md`.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: Criar a estrutura `env-script/` e implementar os scripts base.
  - Entregaveis: Script de iniciar ambiente, script de encerrar ambiente e script de executar testes.
  - Criterio de conclusao: Scripts criados, executaveis e alinhados ao gate de `VIRTUAL_ENV`.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: Validar a integracao dos scripts com o fluxo real do repositorio e com TDD.
  - Entregaveis: Testes automatizados para os scripts ou cobertura equivalente do comportamento esperado, mais ajustes na documentacao.
  - Criterio de conclusao: `pytest -q` passando com cenarios relevantes para os novos scripts.
  - Status: `concluida`

- [x] Fase 4 - Rollout controlado
  - Objetivo: Disponibilizar a nova forma de uso para o time sem quebrar o fluxo manual atual.
  - Entregaveis: README atualizado com exemplos de invocacao e observacoes sobre `source`.
  - Criterio de conclusao: Fluxo recomendado documentado e validado manualmente em shell limpa.
  - Status: `concluida`

- [x] Fase 5 - Estabilizacao e fechamento
  - Objetivo: Consolidar a feature e registrar aprendizados ou limitacoes residuais.
  - Entregaveis: Spec atualizada com status final, riscos remanescentes e historico da entrega.
  - Criterio de conclusao: Fases anteriores concluidas e feature pronta para uso recorrente.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados:
  - Criar primeiro testes que verifiquem os comportamentos esperados dos scripts antes da implementacao, conforme TDD obrigatorio do projeto.
  - Executar `pytest -q` a partir do script dedicado de testes.
- Testes manuais:
  - Validar que o script de iniciar ambiente funciona quando invocado na forma documentada.
  - Validar que o script de encerramento nao promete comportamento impossivel para o shell chamador.
  - Validar mensagens de erro quando `.venv/` nao existir ou quando `pytest` nao estiver disponivel.
- Cenarios de regressao:
  - Garantir que o fluxo manual atual (`source .venv/bin/activate` + comandos) continue funcionando.
  - Garantir que o gate de `VIRTUAL_ENV` continue sendo aplicado antes de comandos de desenvolvimento.

## 7. Rollout e rollback

- Estrategia de rollout:
  - Introduzir `env-script/` como caminho recomendado no `README.md`, mantendo compatibilidade com o fluxo manual existente.
- Estrategia de rollback:
  - Remover a pasta `env-script/` e restaurar a documentacao para o fluxo manual caso os scripts causem ambiguidade operacional.

## 8. Historico de atualizacoes

- 2026-03-09 - Spec criada.
- 2026-03-09 - Contexto da codebase analisado com foco no gate de ambiente virtual, CLI Python atual e ausencia de suite de testes.
- 2026-03-09 - Escopo definido para a nova pasta `env-script/` com scripts de ativacao, encerramento de sessao e execucao de testes.
- 2026-03-09 - `pytest` adicionado ao ambiente virtual e registrado em `requirements.txt` para suportar TDD no repositorio.
- 2026-03-09 - Pasta `env-script/` implementada com `start.sh`, `stop.sh` e `test.sh`.
- 2026-03-09 - Suite inicial em `tests/test_env_scripts.py` criada e validada com `6 passed`.
- 2026-03-09 - README atualizado com o novo fluxo recomendado para ativacao, encerramento e execucao de testes.

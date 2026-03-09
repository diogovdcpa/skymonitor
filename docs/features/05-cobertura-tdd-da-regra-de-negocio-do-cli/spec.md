# Feature 05: Cobertura TDD da regra de negocio do CLI

- ID: `05`
- Slug: `cobertura-tdd-da-regra-de-negocio-do-cli`
- Criada em: 2026-03-09
- Status geral: `concluida`
- Resumo: Adicionar spec e testes automatizados para autenticação, resolução de endpoint e paginação do app.py.

## 1. Objetivo

Reduzir a dependência de validação manual do CLI `app.py` criando cobertura de testes para as regras de negócio que determinam como a aplicação autentica, escolhe endpoint e pagina incidentes. O resultado esperado é uma suíte de unidade que falha primeiro, orienta a implementação e protege regressões sem exigir chamadas reais à API Skyhigh.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `app.py`, que concentra parsing de argumentos, autenticação, escolha de conexão e paginação.
  - `tests/`, hoje restrita aos scripts de ambiente virtual.
- Dependencias tecnicas:
  - `pytest` já disponível via `requirements.txt`.
  - Biblioteca padrão (`unittest.mock`, `argparse`, `json`) para isolar chamadas HTTP.
- Riscos e restricoes:
  - O código atual é monolítico, então os testes precisam atacar funções puras e bordas com mocking sem quebrar o fluxo do CLI.
  - As regras de autenticação possuem múltiplos caminhos (`basic-only`, `legacy`, `skyhigh`, `iam-tenant`, `auto`), o que eleva o risco de lacunas de cobertura.
  - A execução deve respeitar a governança do repositório: TDD obrigatório e testes sempre com venv ativa.

## 3. Referencias externas (opcional, recomendado)

Não aplicável nesta fase. A codebase e a documentação local já fornecem contexto suficiente para estruturar a cobertura inicial.

## 4. Escopo

### Em escopo

- Criar spec da feature com fases curtas de implantação.
- Adicionar testes unitários para `_extract_token`, `_extract_incident_items`, `_extract_next_start_time`, `fetch_all_incidents` e `try_resolve_connection`.
- Cobrir validações de `main()` relacionadas a `incidentCriteria` inválido e exigência de `tenant_id` no modo `iam-tenant`.
- Ajustar `app.py` apenas no necessário para tornar o comportamento testável e estável.

### Fora de escopo

- Testes de integração reais contra endpoints Skyhigh.
- Refatoração arquitetural ampla do CLI para múltiplos módulos.
- Empacotamento Python com `pyproject.toml`.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: mapear o comportamento de negócio atual do CLI e definir o recorte inicial de cobertura.
  - Entregaveis: leitura da codebase, definição do escopo de testes e criação desta spec.
  - Criterio de conclusao: feature criada em `docs/features/05-cobertura-tdd-da-regra-de-negocio-do-cli/spec.md` com fases preenchidas.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: escrever testes vermelhos para as principais regras de negócio e ajustar a implementação mínima necessária.
  - Entregaveis: nova suíte em `tests/` cobrindo autenticação, resolução de conexão, paginação e validações do CLI.
  - Criterio de conclusao: testes novos falhando primeiro e depois passando com mudanças mínimas em `app.py`.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: validar a suíte completa no fluxo oficial do projeto.
  - Entregaveis: execução de `bash env-script/test.sh` com venv ativa e eventuais ajustes finos.
  - Criterio de conclusao: todos os testes relevantes passando sem dependência de rede.
  - Status: `concluida`

- [x] Fase 4 - Rollout controlado
  - Objetivo: documentar o uso da nova cobertura como base para próximas mudanças no CLI.
  - Entregaveis: spec atualizada com status final e critérios de regressão.
  - Criterio de conclusao: documentação refletindo o estado real da implementação.
  - Status: `concluida`

- [x] Fase 5 - Estabilizacao e fechamento
  - Objetivo: encerrar a feature com trilha de auditoria mínima.
  - Entregaveis: histórico de atualizações consolidado e riscos residuais registrados.
  - Criterio de conclusao: spec consistente com o código e a execução final dos testes.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados: `bash env-script/test.sh` com cobertura de `tests/test_app_business_rules.py` e `tests/test_env_scripts.py`.
- Testes manuais: execução opcional de `python app.py --pretty` com `.env` válido para conferir comportamento operacional sem alterar o escopo da feature.
- Cenarios de regressao:
  - queda no fallback entre modos de autenticação;
  - interrupção incorreta da paginação por `nextStartTime`;
  - aceitação indevida de `incidentCriteria` inválido;
  - execução de `iam-tenant` sem `tenant_id`.

## 7. Rollout e rollback

- Estrategia de rollout: incorporar os testes à suíte padrão e usar a cobertura como gate mínimo para novas alterações em `app.py`.
- Estrategia de rollback: reverter apenas a mudança da feature se a nova cobertura expuser incompatibilidade não resolvida, preservando os scripts de ambiente já estáveis.

## 8. Historico de atualizacoes

- 2026-03-09 - Spec criada.
- 2026-03-09 - Descoberta concluída, escopo de cobertura TDD definido e Fase 2 iniciada.
- 2026-03-09 - Testes de regra de negócio adicionados para token, extração de incidentes, paginação, resolução de conexão e validações de `main()`.
- 2026-03-09 - `app.py` ajustado para impedir fallback silencioso para Basic Auth no modo `iam-tenant`.
- 2026-03-09 - Suíte completa validada com `14 passed in 0.58s`.
- 2026-03-09 - Feature renumerada de `04` para `05` para eliminar duplicidade de IDs em `docs/features/`.

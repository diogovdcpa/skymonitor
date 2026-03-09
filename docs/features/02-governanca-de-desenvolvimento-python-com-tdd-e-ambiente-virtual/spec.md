# Feature 02: Governanca de desenvolvimento Python com TDD e ambiente virtual

- ID: `02`
- Slug: `governanca-de-desenvolvimento-python-com-tdd-e-ambiente-virtual`
- Criada em: 2026-03-06
- Status geral: `concluida`
- Resumo: Definir diretrizes em AGENTS.md para Python, TDD obrigatorio e execucao exclusiva em ambiente virtual, com analise e links da codebase.

## 1. Objetivo

Criar um `AGENTS.md` de governanca tecnica para padronizar a evolucao do projeto com foco em Python, exigindo TDD (teste antes da implementacao), conclusao condicionada a testes passando e execucao somente em ambiente virtual ativo.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `AGENTS.md` (novo arquivo de diretrizes de engenharia)
  - `docs/features/02-governanca-de-desenvolvimento-python-com-tdd-e-ambiente-virtual/spec.md`
  - `README.md` e `docs/referencias/skyhigh/*.md` como referencias de contexto
  - `app.py` (CLI Python principal do repositorio)
  - `.env.example` e `requirements.txt` (artefatos de execucao/configuracao ja presentes na raiz)
  - `.codex/skills/documenta/scripts/create_reference_docs.py` (script Python utilitario no ecossistema de skills)
- Dependencias tecnicas:
  - Fluxo de desenvolvimento em Python com `venv`
  - Execucao de testes via `pytest` como criterio de conclusao
  - Documentacao Markdown como meio de governanca
- Riscos e restricoes:
  - A governanca definida em `AGENTS.md` esta mais madura que a estrutura atual de testes: ainda nao existe pasta `tests/` na raiz
  - O repositorio ainda nao possui empacotamento Python com `pyproject.toml`
  - Regras documentadas dependem de adesao operacional ate que haja automacao de enforcement (CI/hooks)

## 3. Referencias externas (opcional, recomendado)

Nao aplicavel nesta entrega. A feature foi definida por politica interna de desenvolvimento e analise local da codebase.

## 4. Escopo

### Em escopo

- Criar `AGENTS.md` na raiz do projeto.
- Registrar regras obrigatorias de Python, TDD e ambiente virtual.
- Definir criterio explicito de conclusao baseado em testes passando.
- Incluir analise da codebase com links para arquivos relevantes do repositorio.

### Fora de escopo

- Criar stack Python completa de execucao (ex.: `pyproject.toml`, empacotamento e pipeline CI).
- Implementar testes automatizados novos para codigo de negocio (nao ha modulo de aplicacao nesta iteracao).
- Alterar o conteudo funcional das referencias Skyhigh em `docs/referencias`.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: Levantar o estado atual da codebase para embasar as diretrizes.
  - Entregaveis: Mapeamento de estrutura, arquivos relevantes e lacunas para fluxo Python.
  - Criterio de conclusao: Diagnostico concluido com riscos e restricoes documentados.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: Criar documento de governanca `AGENTS.md`.
  - Entregaveis: Regras obrigatorias de Python, TDD, criterio de conclusao e uso de venv.
  - Criterio de conclusao: `AGENTS.md` criado com instrucoes operacionais claras.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: Integrar analise da codebase e validar consistencia documental.
  - Entregaveis: Secao de analise com links para artefatos do repositorio e spec atualizada.
  - Criterio de conclusao: Links e diretrizes revisados sem inconsistencias aparentes.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados:
  - Nao aplicavel para esta entrega de governanca documental (sem alteracao de codigo executavel de produto).
- Testes manuais:
  - Revisao do conteudo do `AGENTS.md`.
  - Conferencia dos links da secao de analise da codebase.
  - Verificacao de aderencia ao escopo definido na spec.
- Cenarios de regressao:
  - Risco baixo: alteracoes limitadas a documentacao e processos.
  - Se houver conflito futuro com pipeline real, atualizar o `AGENTS.md` mantendo o principio TDD + venv.

## 7. Rollout e rollback

- Estrategia de rollout:
  - Publicacao direta do `AGENTS.md` na raiz para uso imediato por todos os agentes/contribuidores.
- Estrategia de rollback:
  - Reverter apenas o `AGENTS.md` e esta spec para o estado anterior, sem impacto em runtime de aplicacao.

## 8. Historico de atualizacoes

- 2026-03-06 - Spec criada.
- 2026-03-06 - Analise da codebase concluida com mapeamento de arquivos e lacunas para stack Python.
- 2026-03-06 - `AGENTS.md` criado com politicas de Python, TDD obrigatorio, testes como criterio de conclusao e uso exclusivo de ambiente virtual.
- 2026-03-06 - Fases 1 a 3 marcadas como concluidas e status geral atualizado para `concluida`.
- 2026-03-09 - Contexto da codebase revisado para refletir a existencia de `app.py`, `.env.example` e `requirements.txt` na raiz.

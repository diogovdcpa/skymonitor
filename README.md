# skymonitor

SkyMonitor e um CLI Python para autenticar e consultar incidentes nas APIs do Skyhigh (CASB/DLP). O foco atual do repositorio esta na integracao com endpoints de autenticacao e `queryIncidents`, com suporte a multiplos modos de autenticacao e selecao automatica de host/endpoint.

## Estado atual

- Aplicacao principal em `app.py`
- Configuracao por variaveis de ambiente em `.env`
- Exemplo de configuracao em `.env.example`
- O runtime principal usa apenas biblioteca padrao; o fluxo de testes usa `pytest` documentado em `requirements.txt`
- A configuracao de testes e lint fica centralizada em `pyproject.toml`
- Documentacao de referencia da API em `docs/referencias/skyhigh/`

## Preparacao do ambiente

```bash
python -m venv .venv
source env-script/start.sh
cp .env.example .env
```

Se preferir o fluxo manual, `source .venv/bin/activate` continua valido.

Preencha ao menos:

- `SKY_EMAIL`
- `SKY_PASSWORD`
- `SKY_BASE_URL` ou `SKY_BASE_URLS`
- `SKY_AUTH_MODE`

## Execucao

Exemplo minimo:

```bash
source env-script/start.sh
python app.py
```

Exemplo com menu interativo usando a abertura padrao:

```bash
source env-script/start.sh
python app.py
```

Exemplo com saida JSON no modo legado por argumentos explicitos:

```bash
source env-script/start.sh
python app.py --pretty
```

Exemplo com fluxo IAM por tenant:

```bash
source env-script/start.sh
python app.py --auth-mode iam-tenant --tenant-id SEU_TENANT_ID --pretty
```

## Scripts de ambiente

- `source env-script/start.sh`: ativa a `.venv` na shell atual e valida `VIRTUAL_ENV`.
- `source env-script/stop.sh`: encerra o ambiente virtual na shell atual.
- `bash env-script/test.sh`: executa `pytest -q`, mas exige ambiente virtual ja ativo.
- `bash env-script/lint.sh`: executa `ruff check`, mas exige ambiente virtual ja ativo.
- `bash env-script/typecheck.sh`: executa `mypy`, mas exige ambiente virtual ja ativo.

## Testes atuais

- `tests/test_env_scripts.py`: valida os scripts de ambiente virtual.
- `tests/test_app_business_rules.py`: cobre autenticacao, resolucao de endpoint, validacoes e paginacao.
- `tests/test_app_menu.py`: cobre menu interativo, filtros e janelas de consulta.
- `tests/test_project_governance.py`: valida governanca minima de configuracao e documentacao.

## Capacidades atuais do CLI

- Carrega configuracao automaticamente de `.env`
- Suporta autenticacao `basic-only`, `skyhigh`, `legacy`, `iam-tenant` e `auto`
- Testa combinacoes de base URL e endpoint de incidentes para encontrar uma conexao valida
- Pagina resultados com `nextStartTime`
- Emite JSON em linha unica ou formatado com `--pretty`
- Oferece menu interativo com banner `SkyhighMonitor`
- Abre o menu interativo por padrao quando executado sem argumentos
- Permite consultar todos os incidentes a partir do dia atual ou de uma janela de dias informada
- Permite consultar incidentes `new` de `Microsoft Exchange Online` com filtro local sobre a janela informada
- Permite exportar em CSV os incidentes de `Microsoft Exchange Online` da janela fixa de 1 dia, com paginação completa e deduplicacao por incidente

## Menu interativo

Ao abrir `python app.py` sem argumentos, o menu oferece:

- `1`: trazer todos os incidentes para a janela de dias informada
- `2`: trazer incidentes `new` de `Microsoft Exchange Online` para a janela de dias informada
- `3`: gerar `exchange_incidents_YYYYMMDD.csv` no diretorio atual com colunas `incident_id`, `from` e `to`, usando janela fixa de 1 dia

Na opcao `3`, o CLI consulta todas as paginas disponiveis e remove incidentes repetidos antes de gravar o CSV final.

## Lacunas atuais

- O CLI ainda esta concentrado em `app.py`, misturando transporte HTTP, autenticacao e interface.
- Ainda nao ha pipeline de CI para executar testes e lint automaticamente.
- A validacao operacional final ainda depende de execucao manual com credenciais reais.

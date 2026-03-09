# skymonitor

SkyMonitor e um CLI Python para autenticar e consultar incidentes nas APIs do Skyhigh (CASB/DLP). O foco atual do repositorio esta na integracao com endpoints de autenticacao e `queryIncidents`, com suporte a multiplos modos de autenticacao e selecao automatica de host/endpoint.

## Estado atual

- Aplicacao principal em `app.py`
- Configuracao por variaveis de ambiente em `.env`
- Exemplo de configuracao em `.env.example`
- O runtime principal usa apenas biblioteca padrao; o fluxo de testes usa `pytest` documentado em `requirements.txt`
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

## Capacidades atuais do CLI

- Carrega configuracao automaticamente de `.env`
- Suporta autenticacao `basic-only`, `skyhigh`, `legacy`, `iam-tenant` e `auto`
- Testa combinacoes de base URL e endpoint de incidentes para encontrar uma conexao valida
- Pagina resultados com `nextStartTime`
- Emite JSON em linha unica ou formatado com `--pretty`

## Lacunas atuais

- A suite de testes ainda e inicial e cobre apenas os scripts de ambiente em `tests/`
- Ainda nao ha empacotamento Python com `pyproject.toml`
- A validacao do comportamento hoje depende de execucao manual e das referencias em `docs/`

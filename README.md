# skymonitor

SkyMonitor e um CLI Python para autenticar e consultar incidentes nas APIs do Skyhigh (CASB/DLP). O foco atual do repositorio esta na integracao com endpoints de autenticacao e `queryIncidents`, com suporte a multiplos modos de autenticacao e selecao automatica de host/endpoint.

## Estado atual

- Aplicacao principal em `app.py`
- Configuracao por variaveis de ambiente em `.env`
- Exemplo de configuracao em `.env.example`
- Dependencias externas nao sao necessarias no momento; `requirements.txt` documenta isso explicitamente
- Documentacao de referencia da API em `docs/referencias/skyhigh/`

## Preparacao do ambiente

```bash
python -m venv .venv
source .venv/bin/activate
test -n "$VIRTUAL_ENV" || { echo "Erro: ative um ambiente virtual antes de executar comandos."; exit 1; }
cp .env.example .env
```

Preencha ao menos:

- `SKY_EMAIL`
- `SKY_PASSWORD`
- `SKY_BASE_URL` ou `SKY_BASE_URLS`
- `SKY_AUTH_MODE`

## Execucao

Exemplo minimo:

```bash
source .venv/bin/activate
test -n "$VIRTUAL_ENV" || { echo "Erro: ative um ambiente virtual antes de executar comandos."; exit 1; }
python app.py --pretty
```

Exemplo com fluxo IAM por tenant:

```bash
source .venv/bin/activate
test -n "$VIRTUAL_ENV" || { echo "Erro: ative um ambiente virtual antes de executar comandos."; exit 1; }
python app.py --auth-mode iam-tenant --tenant-id SEU_TENANT_ID --pretty
```

## Capacidades atuais do CLI

- Carrega configuracao automaticamente de `.env`
- Suporta autenticacao `basic-only`, `skyhigh`, `legacy`, `iam-tenant` e `auto`
- Testa combinacoes de base URL e endpoint de incidentes para encontrar uma conexao valida
- Pagina resultados com `nextStartTime`
- Emite JSON em linha unica ou formatado com `--pretty`

## Lacunas atuais

- Ainda nao existe suite de testes em `tests/`
- Ainda nao ha empacotamento Python com `pyproject.toml`
- A validacao do comportamento hoje depende de execucao manual e das referencias em `docs/`

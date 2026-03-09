# AGENTS.md

## Objetivo

Definir o padrao de desenvolvimento para este projeto com foco em Python, qualidade tecnica e previsibilidade de entrega.
Me responda sempre em portugues do brasil.

## Regras obrigatorias

1. Linguagem principal: todo novo desenvolvimento de automacao deve priorizar Python e seguir boas praticas (PEP 8, tipagem quando aplicavel, funcoes pequenas e responsabilidades claras).
2. TDD obrigatorio: sempre escrever um teste antes de implementar a funcao.
3. Criterio de conclusao: uma tarefa so pode ser considerada concluida quando todos os testes relevantes passarem.
4. Ambiente virtual obrigatorio: qualquer comando de desenvolvimento (instalacao, execucao, testes e scripts) so pode ser executado com ambiente virtual ativo.

## Gate de ambiente virtual

Use este gate antes de qualquer comando de desenvolvimento:

```bash
test -n "$VIRTUAL_ENV" || { echo "Erro: ative um ambiente virtual antes de executar comandos."; exit 1; }
```

## Fluxo minimo de trabalho

1. Criar a venv se necessario (`python -m venv .venv`).
2. Ativar o ambiente com `source env-script/start.sh` (ou `source .venv/bin/activate` no fluxo manual).
3. Escrever teste inicial para o comportamento esperado (teste deve falhar primeiro).
4. Implementar a funcao.
5. Executar testes com `bash env-script/test.sh` (ou `pytest -q` com a venv ativa).
6. Encerrar o ambiente com `source env-script/stop.sh` ao finalizar a sessao, quando aplicavel.
7. Finalizar somente com testes passando.

## Scripts de ambiente

- Iniciar ambiente virtual: `source env-script/start.sh`
- Executar testes: `bash env-script/test.sh`
- Encerrar ambiente virtual: `source env-script/stop.sh`

Observacao importante:

- Os scripts `start.sh` e `stop.sh` devem ser executados com `source` para afetarem a shell atual.

## Analise da codebase (2026-03-09)

Estado atual do repositorio:

- O projeto possui um CLI Python funcional na raiz (`app.py`) para autenticacao e consulta de incidentes na API Skyhigh.
- A raiz ja contem artefatos basicos de execucao Python (`requirements.txt` e `.env.example`), embora ainda nao exista empacotamento com `pyproject.toml`.
- O repositorio continua fortemente orientado a documentacao tecnica em Markdown e referencias operacionais.
- O repositorio ja possui uma suite inicial em `tests/` para validar os scripts de ambiente virtual.
- A raiz agora inclui a pasta `env-script/` com scripts para ativacao, testes e encerramento da sessao de desenvolvimento.
- Existem scripts utilitarios adicionais no ecossistema de skills local.

Arquivos e pontos principais:

- [README.md](README.md)
- [app.py](app.py)
- [requirements.txt](requirements.txt)
- [env-script/start.sh](env-script/start.sh)
- [env-script/stop.sh](env-script/stop.sh)
- [env-script/test.sh](env-script/test.sh)
- [tests/test_env_scripts.py](tests/test_env_scripts.py)
- [.env.example](.env.example)
- [docs/referencias/skyhigh/index.md](docs/referencias/skyhigh/index.md)
- [docs/referencias/skyhigh/06-troubleshooting-e-boas-praticas.md](docs/referencias/skyhigh/06-troubleshooting-e-boas-praticas.md)
- [docs/features/01-correcao-de-yaml-no-skill-documenta/spec.md](docs/features/01-correcao-de-yaml-no-skill-documenta/spec.md)
- [docs/features/02-governanca-de-desenvolvimento-python-com-tdd-e-ambiente-virtual/spec.md](docs/features/02-governanca-de-desenvolvimento-python-com-tdd-e-ambiente-virtual/spec.md)
- [.codex/skills/documenta/scripts/create_reference_docs.py](.codex/skills/documenta/scripts/create_reference_docs.py)
- [.codex/skills/feature/scripts/create_feature.sh](.codex/skills/feature/scripts/create_feature.sh)

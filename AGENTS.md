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

1. Criar e ativar venv (`python -m venv .venv` e `source .venv/bin/activate`).
2. Escrever teste inicial para o comportamento esperado (teste deve falhar primeiro).
3. Implementar a funcao.
4. Executar testes (`pytest -q`).
5. Finalizar somente com testes passando.

## Analise da codebase (2026-03-06)

Estado atual do repositorio:

- O projeto esta majoritariamente estruturado como documentacao tecnica em Markdown.
- Nao ha, neste momento, estrutura Python de aplicacao pronta para execucao (`pyproject.toml`, `requirements*.txt` e pasta `tests/` nao encontrados na raiz).
- Existe script Python utilitario no ecossistema de skills local.

Arquivos e pontos principais:

- [README.md](README.md)
- [docs/referencias/skyhigh/index.md](docs/referencias/skyhigh/index.md)
- [docs/referencias/skyhigh/06-troubleshooting-e-boas-praticas.md](docs/referencias/skyhigh/06-troubleshooting-e-boas-praticas.md)
- [docs/features/01-correcao-de-yaml-no-skill-documenta/spec.md](docs/features/01-correcao-de-yaml-no-skill-documenta/spec.md)
- [docs/features/02-governanca-de-desenvolvimento-python-com-tdd-e-ambiente-virtual/spec.md](docs/features/02-governanca-de-desenvolvimento-python-com-tdd-e-ambiente-virtual/spec.md)
- [.codex/skills/documenta/scripts/create_reference_docs.py](.codex/skills/documenta/scripts/create_reference_docs.py)
- [.codex/skills/feature/scripts/create_feature.sh](.codex/skills/feature/scripts/create_feature.sh)

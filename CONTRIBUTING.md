# Contribuindo

Este repositório segue um GitHub Flow enxuto para manter entregas rápidas e histórico limpo.

## Branches

- `main`: sempre estável e pronta para produção.
- `feature/<nome-curto>`: nova funcionalidade.
- `fix/<nome-curto>`: correção de bug.

Nao faca push direto na `main`.

## Commits

Prefira commits atomicos (uma intencao logica por commit).

Formato recomendado:

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`

Exemplo:

- `feat: adiciona validacao de workflow no CI`

## Pull Request

Abra PR da sua branch para `main` usando o template em `.github/pull_request_template.md`.

Checklist minimo:

1. Rebase com `main` concluido.
2. Commits claros e atomicos.
3. CI verde.
4. Validacao manual descrita no PR.

## Fluxo rapido

```bash
# criar branch
git checkout -b feature/nome-curto

# manter a branch atualizada
git fetch origin
git rebase origin/main

# enviar branch
git push -u origin feature/nome-curto
```

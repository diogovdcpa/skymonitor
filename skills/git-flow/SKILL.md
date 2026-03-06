---
name: git-flow
description: Padronizar colaboração Git em equipes pequenas com foco em velocidade e organização. Usar quando for definir ou aplicar fluxo de branches, pull requests, commits, rebase, revisão leve de código, automações de CI básicas e documentação de contribuição (README/CONTRIBUTING).
---

# Git Flow

## Objetivo

Aplicar um fluxo Git simples e previsível para times pequenos, evitando burocracia e histórico confuso.

## Workflow Base

Usar GitHub Flow:

1. Manter `main` sempre estável e pronta para produção.
2. Criar uma branch por tarefa:
- `feature/<nome-curto>` para funcionalidade.
- `fix/<nome-curto>` para correção.
3. Finalizar a tarefa e abrir pull request para `main`.
4. Fazer merge apenas após revisão rápida.

Não fazer push direto na `main`.

## Pull Request e Review Leve

Tratar PR como registro técnico da mudança.

No PR:

1. Explicar problema e solução em poucas linhas.
2. Destacar impacto, risco e como validar.
3. Revisar de forma objetiva (bug óbvio, regressão, legibilidade).
4. Compartilhar aprendizado técnico quando houver simplificação relevante.

## Padrão de Commits

Criar commits atômicos: uma intenção lógica por commit.

Mensagens:

1. Usar verbo no imperativo.
2. Evitar mensagens genéricas.
3. Preferir Conventional Commits quando possível:
- `feat:` nova funcionalidade
- `fix:` correção
- `docs:` documentação

Exemplos:

- `feat: adiciona login social com Google`
- `fix: corrige quebra de layout no header mobile`
- `docs: documenta setup local no README`

## Histórico Limpo

Preferir `rebase` para manter histórico linear.

Antes de abrir/finalizar PR:

1. Atualizar `main` local.
2. Rebasear a branch de trabalho com `main`.
3. Resolver conflitos localmente.
4. Executar testes/lint novamente.

## Automação Mínima Obrigatória

Configurar CI para validar PR automaticamente:

1. Linter/formatter (ex.: ESLint, Prettier, Ruff, Black).
2. Testes automatizados.
3. Bloqueio de merge quando validações falharem.

Priorizar GitHub Actions para pipeline inicial por simplicidade.

## Comandos Essenciais

```bash
# criar branch da tarefa
git checkout -b feature/nome-da-branch

# atualizar branch local sem merge commit
git pull --rebase origin main

# salvar trabalho temporariamente
git stash

# visualizar histórico linear
git log --oneline --graph --all
```

## Checklist de Aplicação

Antes de mergear:

1. Confirmar que não houve push direto na `main`.
2. Garantir commits atômicos e mensagens claras.
3. Verificar rebase com `main` concluído.
4. Confirmar PR com contexto suficiente.
5. Confirmar CI verde.
6. Atualizar `README.md` e `CONTRIBUTING.md` se processo mudou.

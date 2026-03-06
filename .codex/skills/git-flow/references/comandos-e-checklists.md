# Comandos e Checklists

## Comandos Recomendados

| Acao | Comando |
| --- | --- |
| Criar branch nova | `git checkout -b feature/nome-da-feature` |
| Atualizar com main | `git fetch origin && git rebase origin/main` |
| Salvar alteracoes temporarias | `git stash` |
| Recuperar alteracoes do stash | `git stash pop` |
| Ver historico linear | `git log --oneline --graph --all` |
| Enviar branch ao remoto | `git push -u origin <branch>` |
| Apagar branch local (apos merge) | `git branch -d <branch>` |

## Checklist: Inicio de Branch

- Confirmar que `main` local esta atualizada
- Criar branch com prefixo correto (`feature/`, `fix/`, `docs/`, `chore/`)
- Definir escopo pequeno e objetivo

## Checklist: Antes do PR

- Rebase com `origin/main` finalizado sem conflitos pendentes
- Commits atômicos e com mensagem clara
- Testes locais executados
- Lint/format executados
- Descricao do PR com contexto, mudanca e validacao

## Checklist: Revisao Leve

- Verificar risco de regressao
- Verificar cobertura de casos principais
- Conferir legibilidade da mudanca
- Confirmar estrategia de rollback em mudancas sensiveis

## Checklist: Encerramento da Branch

- Confirmar merge do PR na `main`
- Atualizar `main` local (`git checkout main && git pull --rebase origin main`)
- Apagar branch local (`git branch -d <branch>`)

## Templates Prontos (Copiar e Colar)

### 1) Branch de Trabalho

```bash
git checkout main
git pull --rebase origin main
git checkout -b feature/nome-curto-da-tarefa
```

### 2) Commit (Conventional Commits)

```text
feat: adiciona monitoramento de anomalias por regra
fix: corrige filtro de incidentes duplicados
docs: atualiza fluxo de contribuicao no README
chore: ajusta automacao de validacao no CI
```

### 3) Descricao de PR

```md
## Problema
Precisamos [descrever o problema real em 1-2 linhas].

## Solucao
Foi implementado [resumo objetivo da mudanca].

## Como testar
1. Executar [comando/fluxo principal].
2. Validar [resultado esperado].
3. Confirmar que [caso de borda/regressao] permanece correto.

## Risco e rollback
Risco baixo/moderado porque [motivo].
Rollback: reverter o PR ou o commit [hash] se necessario.
```

### 4) Fechamento da Tarefa (apos merge)

```bash
git checkout main
git pull --rebase origin main
git branch -d feature/nome-curto-da-tarefa
```

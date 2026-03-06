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

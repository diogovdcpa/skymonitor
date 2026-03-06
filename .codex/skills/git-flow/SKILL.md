---
name: git-flow
description: Padroniza o fluxo de GitHub Flow para times pequenos, com criação de branches de feature/fix, commits atômicos com Conventional Commits, PR leve com revisão rápida, atualização via rebase e automação mínima de qualidade. Use quando o usuário pedir organização de branches, estratégia de merge/rebase, boas práticas de PR, mensagens de commit e setup de CI básico em repositórios Git.
---

# GitHub Flow Para Times Pequenos

## Objetivo

Aplicar um fluxo simples e consistente para manter a `main` estável e o histórico limpo.
Priorizar produtividade com pouca burocracia em equipes pequenas.

## Workflow Padrão

1. Proteger `main`:
- Não fazer push direto.
- Aceitar mudanças via Pull Request.

2. Criar branch por tarefa:
- Usar prefixos `feature/`, `fix/`, `docs/`, `chore/`.
- Exemplo: `feature/login-social`, `fix/header-overflow`.

3. Commits atômicos:
- Cada commit representa uma unidade lógica única.
- Evitar commits grandes com mudanças não relacionadas.

4. Escrever mensagens claras:
- Preferir formato imperativo.
- Sempre que possível usar Conventional Commits:
  - `feat:`
  - `fix:`
  - `docs:`
  - `chore:`

5. Atualizar branch com rebase:
- Antes de abrir/finalizar PR, sincronizar com `main`.
- Resolver conflitos localmente para reduzir ruído no PR.

6. Abrir PR curto e revisável:
- Explicar contexto, mudança e impacto.
- Focar review em bugs, regressões e clareza.

7. Validar com automação:
- Rodar lint, format e testes no PR (CI).

## Decisões Operacionais

- Preferir `rebase` para manter histórico linear.
- Evitar `merge commits` em excesso para tarefas pequenas.
- Se a mudança for urgente e pequena, ainda abrir PR curto.
- Se houver conflito recorrente, quebrar features em branches menores.

## Pull Request Leve

- Exigir template simples:
  - Problema
  - Solução
  - Como testar
  - Risco/rollback
- Limitar escopo por PR para facilitar revisão.
- Incentivar revisão em dupla/trio com foco técnico objetivo.

## Comandos Essenciais

Consultar [`references/comandos-e-checklists.md`](references/comandos-e-checklists.md) para:
- comandos recomendados;
- checklist de início de branch;
- checklist antes do PR;
- checklist de revisão.

## Automação Mínima Recomendada

- Sugerir GitHub Actions para executar:
  - lint;
  - testes automatizados;
  - validação de build (quando aplicável).
- Bloquear merge na `main` se checks obrigatórios falharem.

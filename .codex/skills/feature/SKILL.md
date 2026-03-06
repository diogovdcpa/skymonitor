---
name: feature
description: Planejar e iniciar novas features com leitura da codebase e, quando util, pesquisa na web para padroes, tecnicas e boas praticas atualizadas, criando especificacoes versionadas em `docs/features/NN-nome-da-feature/spec.md` com template padrao e ate 5 fases de implantacao. Use quando o usuario pedir para criar uma nova feature, montar plano incremental de implementacao, ou atualizar o progresso de fases de uma feature existente.
---

# Feature

## Objetivo

Padronizar a criacao e manutencao de specs de feature com contexto tecnico real da codebase, complemento opcional por pesquisa na web e plano de execucao em fases curtas.

## Fluxo Padrao

1. Ler o contexto do projeto antes de escrever a spec.
- Mapear a estrutura com `rg --files`.
- Ler arquivos de entrada relevantes (ex.: `README*`, `package.json`, `pyproject.toml`, `go.mod`, `src/*`, `app/*`, `docs/*`).
- Identificar modulos afetados e riscos tecnicos da feature.

2. Quando agregar valor, pesquisar referencias atuais na web.
- Buscar padroes consolidados, tecnicas de implementacao e boas praticas recentes.
- Priorizar fontes oficiais (documentacao primaria, RFCs, guias de mantenedores).
- Incorporar na spec apenas o que for relevante para o contexto real da codebase.

3. Definir o nome da feature e o slug.
- Nome: legivel para produto/time.
- Slug: kebab-case tecnico (ex.: `alert-routing`).

4. Criar a estrutura da feature com script.

```bash
bash .codex/skills/feature/scripts/create_feature.sh "Nome da Feature" "Resumo opcional"
```

- O script cria `docs/features/NN-slug/`.
- O script cria `docs/features/NN-slug/spec.md` a partir do template oficial.
- A numeracao `NN` e automatica e incremental (`01`, `02`, `03`...).

5. Completar a spec com contexto real da codebase.
- Preencher objetivo, escopo, impacto tecnico, validacao e rollout.
- Referenciar componentes/arquivos reais para reduzir ambiguidade.
- Se houver pesquisa web, sintetizar os padroes adotados e justificar as escolhas.

6. Planejar implementacao em ate 5 fases.
- Nunca ultrapassar 5 fases.
- Se o trabalho for maior, agrupar por entregas de valor e reduzir granularidade.
- Cada fase precisa conter objetivo, entregaveis e criterio de conclusao.

7. Atualizar status durante a execucao.
- Marcar checkbox da fase como concluida (`[x]`).
- Atualizar campo `Status` da fase (`nao iniciada`, `em andamento`, `concluida`, `bloqueada`).
- Registrar mudancas em `Historico de atualizacoes` com data.

## Regras Obrigatorias

- Criar specs somente no padrao `docs/features/NN-slug/spec.md`.
- Manter uma estrutura unica de spec com o template em `references/spec-template.md`.
- Limitar o plano a no maximo 5 fases.
- Atualizar a spec ao longo da implementacao, sem deixar o status desatualizado.

## Recursos

- Script de criacao: `scripts/create_feature.sh`
- Template oficial: `references/spec-template.md`

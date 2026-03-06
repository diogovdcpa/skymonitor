# Feature 01: Correcao de YAML no SKILL documenta

- ID: `01`
- Slug: `correcao-de-yaml-no-skill-documenta`
- Criada em: 2026-03-06
- Status geral: `concluida`
- Resumo: Corrigir front matter do skill documenta para eliminar erro de parse YAML no carregamento de skills.

## 1. Objetivo

Eliminar o erro de parse YAML no carregamento de skills para que o skill `documenta` seja carregado sem skip, reduzindo falhas operacionais e ruido no bootstrap do ambiente.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `.codex/skills/documenta/SKILL.md` (front matter)
  - Descoberta de skills no bootstrap do ambiente Codex
- Dependencias tecnicas:
  - Parser YAML usado pelo carregador de skills
  - Delimitadores de front matter `---`
- Riscos e restricoes:
  - Variacao de compatibilidade entre parsers YAML (estritos vs. completos)
  - Mudancas no texto de descricao nao devem alterar a finalidade do skill

## 3. Referencias externas (opcional, recomendado)

Nao aplicavel nesta entrega. Mudanca local sem dependencia de padroes externos.

## 4. Escopo

### Em escopo

- Normalizar `description` do front matter para string simples e explicitamente delimitada.
- Remover elementos que podem gerar ambiguidade em parsers YAML mais estritos (formato multiline/folding e markdown inline no metadata).
- Atualizar a spec com status por fase e historico da entrega.

### Fora de escopo

- Alteracoes de comportamento dos scripts Python/Bash dos skills.
- Reestruturacao de outros `SKILL.md` que nao apresentaram erro.
- Mudancas em prompts, templates ou fluxo funcional do skill `documenta`.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: Identificar causa provavel do erro de parse e definir formato de front matter compativel.
  - Entregaveis: Diagnostico do arquivo alvo e estrategia de normalizacao do metadata.
  - Criterio de conclusao: Caminho de correcao definido sem alterar o conteudo funcional do skill.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: Aplicar correcao direta no `SKILL.md` do `documenta`.
  - Entregaveis: Front matter atualizado para descricao em string unica entre aspas.
  - Criterio de conclusao: Arquivo salvo com estrutura YAML simples e consistente.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: Verificar consistencia estrutural do front matter e fechar documentacao da feature.
  - Entregaveis: Revisao do arquivo final e spec preenchida com escopo, validacao e historico.
  - Criterio de conclusao: Nenhuma inconsistencia estrutural aparente no arquivo corrigido.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados: Nao ha suite automatizada de validacao de front matter neste repositorio.
- Testes manuais:
  - Inspecao linha a linha do bloco YAML inicial do `SKILL.md`.
  - Confirmacao de delimitadores `---` e pares `chave: valor`.
- Cenarios de regressao:
  - Confirmar que o skill continua legivel e semanticamente equivalente no catalogo de skills.

## 7. Rollout e rollback

- Estrategia de rollout: Alteracao direta e imediata no arquivo do skill.
- Estrategia de rollback: Reverter apenas `.codex/skills/documenta/SKILL.md` para o estado anterior em caso de erro de carregamento.

## 8. Historico de atualizacoes

- 2026-03-06 - Spec criada.
- 2026-03-06 - Front matter do `documenta/SKILL.md` normalizado para formato mais compativel com parser YAML estrito.
- 2026-03-06 - Fases 1 a 3 marcadas como concluidas.

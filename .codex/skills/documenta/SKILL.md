---
name: documenta
description: >-
  Criar documentacao tecnica em Markdown a partir de um arquivo-base enviado pelo usuario,
  organizando o conteudo em secoes menores e mantendo um documento principal consolidado em
  `docs/referencias/<nome>/index.md`. Use quando o usuario pedir para transformar manuais, guias,
  politicas, configuracoes ou qualquer referencia em docs `.md` estruturadas por topico, com pasta
  dedicada por nome principal (ex.: `fortinet`).
---

# Documenta

## Objetivo

Padronizar a criacao de documentacao em `docs/referencias/<nome>/` com:
- arquivo principal `index.md`;
- secoes quebradas em multiplos arquivos `NN-topico.md`;
- importacao consolidada das secoes no principal.

## Entradas Minimas

1. `arquivo_fonte`:
- Caminho do arquivo enviado pelo usuario com o conteudo base.

2. `nome_principal`:
- Nome da referencia principal (ex.: `fortinet`).
- Esse nome vira a pasta: `docs/referencias/<nome_principal>/`.

## Fluxo Padrao

1. Ler o arquivo enviado.
- Identificar publico, escopo e topicos.
- Se o arquivo for muito grande, separar entre 3 e 8 secoes.

2. Criar estrutura base com script:

```bash
python .codex/skills/documenta/scripts/create_reference_docs.py \
  --name "<nome_principal>" \
  --source "<arquivo_fonte>" \
  --section "Visao geral" \
  --section "Arquitetura" \
  --section "Configuracao" \
  --section "Operacao" \
  --section "Troubleshooting"
```

- O comando cria:
  - `docs/referencias/<nome_principal>/index.md` (principal);
  - `docs/referencias/<nome_principal>/NN-topico.md` (secoes).

3. Preencher cada secao com base no arquivo fonte.
- Escrever conteudo objetivo, sem repetir o arquivo original literalmente.
- Priorizar passos praticos, exemplos e checkpoints.

4. Regerar o principal com importacao consolidada:

```bash
python .codex/skills/documenta/scripts/create_reference_docs.py \
  --name "<nome_principal>" \
  --source "<arquivo_fonte>"
```

- O script atualiza o `index.md` com:
  - sumario das secoes;
  - bloco de conteudo importado (concatenacao das secoes).

5. Validar qualidade final.
- Conferir links internos e ordem das secoes.
- Garantir que cada secao tenha foco unico.
- Ajustar titulos para facilitar busca e navegacao.

## Regras Obrigatorias

- Sempre usar `docs/referencias/<nome_principal>/`.
- Sempre manter `index.md` como documento principal.
- Sempre quebrar documentos extensos em arquivos `NN-topico.md`.
- Sempre atualizar o principal com sumario + bloco consolidado importado.
- Nunca apagar manualmente secoes existentes sem confirmar com o usuario.

## Recursos

- Script principal: `scripts/create_reference_docs.py`
- Guia de estrutura: `references/estrutura.md`

## Exemplo Rapido

Usuario:
- "Documenta esse guia e usa nome principal `fortinet`."

Saida esperada:
- `docs/referencias/fortinet/index.md`
- `docs/referencias/fortinet/01-visao-geral.md`
- `docs/referencias/fortinet/02-arquitetura.md`
- `docs/referencias/fortinet/03-configuracao.md`
- `docs/referencias/fortinet/04-operacao.md`
- `docs/referencias/fortinet/05-troubleshooting.md`

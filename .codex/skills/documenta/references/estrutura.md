# Estrutura Recomendada

Usar este guia para manter consistencia entre documentacoes geradas pela skill `documenta`.

## Layout Base

Cada documentacao deve seguir:

- `docs/referencias/<nome>/index.md`:
  - arquivo principal com sumario e conteudo importado.
- `docs/referencias/<nome>/NN-topico.md`:
  - secoes menores para facilitar leitura e manutencao.

## Tamanho E Divisao

- Dividir o conteudo em secoes quando o arquivo ficar grande.
- Mirar em secoes com foco unico.
- Preferir 3 a 8 secoes para uma primeira versao.

## Checklist De Qualidade

- Titulos claros e consistentes.
- Passos operacionais com ordem logica.
- Termos tecnicos padronizados.
- Links internos funcionando.
- Sem duplicacao desnecessaria entre secoes.

## Padrao De Secao

Cada arquivo de secao pode seguir:

```md
# NN - Nome da secao

## Objetivo

## Conteudo

## Referencias
```

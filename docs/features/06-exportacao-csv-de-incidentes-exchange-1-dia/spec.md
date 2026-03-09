# Feature 06: Exportacao CSV de incidentes Exchange 1 dia

- ID: `06`
- Slug: `exportacao-csv-de-incidentes-exchange-1-dia`
- Criada em: 2026-03-09
- Status geral: `concluida`
- Resumo: Adicionar uma opcao no menu para exportar todos os incidentes do Microsoft Exchange Online da janela de 1 dia em CSV, com paginacao completa e deduplicacao por incidente.

## 1. Objetivo

Adicionar uma terceira opcao ao menu interativo para exportar em CSV todos os incidentes de Microsoft Exchange Online da janela de 1 dia.

O resultado esperado e um arquivo CSV gerado localmente com as colunas `incident_id`, `from` e `to`, cobrindo todas as paginas retornadas pela API e removendo incidentes repetidos quando a pagina seguinte reapresentar registros ja vistos.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `skymonitor/cli.py` contem o menu interativo, a orquestracao das consultas e a formatacao da saida textual.
  - `skymonitor/api.py` concentra a paginacao por `nextStartTime`, sendo o ponto correto para a deduplicacao entre paginas.
  - `tests/test_app_menu.py` cobre o comportamento do menu e precisa validar a nova opcao de exportacao.
  - `tests/test_app_business_rules.py` cobre regras da API, incluindo paginacao, e precisa validar a deduplicacao.
- Dependencias tecnicas:
  - O runtime continua restrito a biblioteca padrao, entao a exportacao deve usar `csv` e `pathlib`.
  - A API ja possui paginação baseada em `nextStartTime`; a nova feature deve reutilizar esse fluxo sem criar um segundo coletor HTTP.
  - O menu ja recebe `now` injetavel nos testes, o que permite gerar nome de arquivo deterministico para TDD.
- Riscos e restricoes:
  - A API pode repetir incidentes entre paginas; sem deduplicacao o CSV final ficaria inconsistente.
  - Nem todo incidente necessariamente expoe `from` e `to` no mesmo nivel; a exportacao precisa tolerar ausencia de campos.
  - O menu atual pede quantidade de dias para as opcoes 1 e 2; a opcao 3 deve fixar 1 dia para manter aderencia ao pedido e evitar ambiguidade operacional.

## 3. Referencias externas (opcional, recomendado)

Usar esta secao quando houver pesquisa na web para embasar decisoes tecnicas.

- Fonte:
- Link:
- Data de acesso:
- Insight aplicado na feature:

## 4. Escopo

### Em escopo

- Adicionar opcao `3` no menu interativo para exportacao CSV de incidentes de Microsoft Exchange Online.
- Fixar a janela da exportacao em 1 dia, calculada com a mesma regra ja usada no CLI.
- Reaproveitar a consulta existente e aplicar filtro local para incidentes de Microsoft Exchange Online, independentemente do status.
- Gerar arquivo CSV local com colunas `incident_id`, `from` e `to`.
- Deduplicar incidentes durante a paginação usando chave de incidente para evitar linhas repetidas no arquivo final.
- Exibir no menu o caminho do CSV gerado e a quantidade de incidentes exportados.
- Cobrir a feature com testes automatizados de menu, exportacao e deduplicacao.

### Fora de escopo

- Parametrizacao do caminho do CSV por prompt ou argumento de linha de comando.
- Exportacao de colunas adicionais alem de `incident_id`, `from` e `to`.
- Alteracao das opcoes ja existentes do menu.
- Persistencia de historico de exportacoes.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: mapear os pontos de extensao do menu e da paginação para incluir exportacao CSV sem duplicacao.
  - Entregaveis: escopo fechado, estrategia de deduplicacao por incidente e cenarios de teste definidos.
  - Criterio de conclusao: spec atualizada com modulos impactados, riscos e definicao do comportamento da opcao 3.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: implementar filtro Exchange, geracao do CSV e nova opcao no menu.
  - Entregaveis: helpers de exportacao, nome de arquivo padrao, opcao `3` e mensagens de saida.
  - Criterio de conclusao: usuario consegue executar a opcao no menu e obter um CSV valido em disco.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: garantir paginação completa sem repeticao de linhas no CSV final.
  - Entregaveis: deduplicacao durante `fetch_all_incidents` e testes automatizados de regressao.
  - Criterio de conclusao: paginas repetidas nao geram duplicatas e todos os testes relevantes passam.
  - Status: `concluida`

- [x] Fase 4 - Rollout controlado
  - Objetivo: documentar a nova opcao operacional.
  - Entregaveis: README atualizado com o fluxo de exportacao CSV pelo menu.
  - Criterio de conclusao: operador consegue executar a exportacao lendo apenas a documentacao.
  - Status: `concluida`

- [x] Fase 5 - Estabilizacao e fechamento
  - Objetivo: consolidar a entrega com testes finais e status atualizado.
  - Entregaveis: suite relevante verde, ajustes finais e historico preenchido.
  - Criterio de conclusao: feature concluida com comportamento coberto por testes e spec refletindo o estado final.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados:
  - teste de paginação com incidentes repetidos entre paginas;
  - teste de filtro local para Exchange Online;
  - teste da opcao `3` do menu gerando CSV com conteudo esperado.
- Testes manuais:
  - abrir o menu e acionar a opcao `3`;
  - validar criacao do arquivo CSV no diretorio atual;
  - abrir o CSV e conferir colunas `incident_id`, `from` e `to`.
- Cenarios de regressao:
  - opcoes `1` e `2` continuam funcionando com prompt de dias;
  - o modo JSON legado por argumentos continua inalterado;
  - a paginação continua trazendo todos os incidentes sem loop infinito.

## 7. Rollout e rollback

- Estrategia de rollout:
  - liberar a nova opcao apenas no menu interativo, sem alterar o fluxo atual por argumentos;
  - validar primeiro em janela curta de 1 dia para limitar risco operacional.
- Estrategia de rollback:
  - remover a opcao `3` do menu e os helpers de exportacao;
  - manter a deduplicacao de paginação se ela for considerada correcao de integridade util para o fluxo existente.

## 8. Historico de atualizacoes

- 2026-03-09 - Spec criada.
- 2026-03-09 - Fase 1 colocada em andamento com escopo definido para opcao de exportacao CSV, filtro Exchange e deduplicacao entre paginas.
- 2026-03-09 - Fases 1 a 5 concluidas com implementacao da opcao 3 do menu, exportacao `exchange_incidents_YYYYMMDD.csv`, deduplicacao por incidente durante a paginacao e validacao completa com testes, lint e mypy.

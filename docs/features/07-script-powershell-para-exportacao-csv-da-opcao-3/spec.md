# Feature 07: Script PowerShell para exportacao CSV da opcao 3

- ID: `07`
- Slug: `script-powershell-para-exportacao-csv-da-opcao-3`
- Criada em: 2026-03-10
- Status geral: `concluida`
- Resumo: Extrair a opcao 3 do CLI para um script PowerShell que exibe o banner, le credenciais de um .env minimo e gera o CSV no diretorio atual.

## 1. Objetivo

Disponibilizar um fluxo operacional independente do CLI Python para executar apenas a exportacao CSV hoje coberta pela opcao `3` do menu interativo.

O resultado esperado e um script PowerShell que:
- exibe o banner `SkyhighMonitor` durante a execucao;
- le apenas as configuracoes minimas de autenticacao a partir de um arquivo `.env` simples;
- consulta os incidentes de Microsoft Exchange Online da janela fixa de 1 dia;
- gera um arquivo `.csv` no diretorio em que o usuario executou o script.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `skymonitor/cli.py` ja implementa a opcao `3` do menu com banner, janela fixa de 1 dia e exportacao de CSV no diretorio corrente.
  - `skymonitor/api.py` concentra autenticacao, descoberta de endpoint, consulta paginada e filtros de incidentes; essa regra deve ser reutilizada como referencia funcional da feature.
  - `tests/test_app_menu.py` e `tests/test_app_business_rules.py` ja cobrem o comportamento atual da opcao `3`, servindo de base para preservar compatibilidade funcional.
  - `README.md` e `.env.example` precisarao orientar o novo fluxo para usuarios Windows com um `.env` reduzido ao necessario.
- Dependencias tecnicas:
  - O projeto atual e Python-first, mas esta feature introduz um artefato operacional em PowerShell (`.ps1`) para consumo direto pelo usuario final.
  - O script PowerShell deve reproduzir o banner existente e escrever o CSV com as colunas `incident_id`, `from` e `to`, preservando o contrato ja adotado no Python.
  - O `.env` minimo deve evitar configuracoes opcionais desnecessarias; o baseline esperado e `SKY_BASE_URL`, `SKY_EMAIL` e `SKY_PASSWORD`, com avaliacao se `SKY_AUTH_MODE=basic-only` entra como default interno do script.
  - O arquivo de saida deve ser criado com base em `Get-Location`, sem depender do diretorio do script.
- Riscos e restricoes:
  - Duplicar regras de autenticacao e paginacao em PowerShell pode gerar divergencia futura com o comportamento do modulo Python.
  - O parser de `.env` em PowerShell precisa tolerar comentarios, linhas em branco e valores simples sem introduzir dependencia externa.
  - O script deve deixar claro quais variaveis sao obrigatorias para evitar falhas silenciosas de autenticacao.
  - O projeto possui governanca com TDD; a implementacao precisa nascer com testes antes do codigo novo e concluir apenas com a suite relevante verde.

## 3. Referencias externas (opcional, recomendado)

Usar esta secao quando houver pesquisa na web para embasar decisoes tecnicas.

- Nao utilizado nesta abertura.

## 4. Escopo

### Em escopo

- Criar um script PowerShell dedicado para a exportacao equivalente a opcao `3` do menu.
- Exibir o banner `SkyhighMonitor` no inicio do fluxo e mensagens de progresso durante a execucao.
- Ler credenciais e configuracoes minimas de um arquivo `.env` simples no formato `CHAVE=valor`.
- Consultar apenas incidentes de Microsoft Exchange Online na janela fixa de 1 dia.
- Gerar CSV no diretorio atual de execucao com nome padrao deterministico.
- Preservar as colunas `incident_id`, `from` e `to` do arquivo exportado.
- Documentar o uso do `.ps1`, o formato minimo do `.env` e o local esperado do arquivo de saida.
- Cobrir o fluxo novo com testes automatizados compativeis com a politica de TDD do repositorio.

### Fora de escopo

- Substituir ou remover a opcao `3` existente no CLI Python.
- Reescrever todas as demais opcoes do menu em PowerShell.
- Suportar filtros adicionais, quantidade de dias configuravel ou exportacao para formatos alem de CSV.
- Introduzir dependencias externas de PowerShell Gallery ou modulos de terceiros.
- Implementar interface grafica para selecao de credenciais ou caminho de saida.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: consolidar o contrato funcional da opcao `3` e definir como ele sera espelhado em PowerShell sem ambiguidade.
  - Entregaveis: mapeamento dos campos do CSV, variaveis minimas do `.env`, estrategia de autenticacao e abordagem de testes.
  - Criterio de conclusao: spec refinada com entradas, saidas, riscos e criterio de compatibilidade funcional.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: implementar o script `.ps1` com banner, leitura do `.env`, autenticacao e exportacao CSV no diretorio atual.
  - Entregaveis: script PowerShell principal, parser simples de `.env` e geracao do arquivo `exchange_incidents_YYYYMMDD.csv` ou equivalente definido.
  - Criterio de conclusao: usuario consegue executar o script e obter um CSV valido sem abrir o CLI Python interativo.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: garantir aderencia ao comportamento atual da opcao `3` e evitar regressao na regra de negocio.
  - Entregaveis: testes automatizados do novo fluxo, validacao de colunas e verificacao do destino do arquivo.
  - Criterio de conclusao: o comportamento do `.ps1` fica coberto por testes e coerente com a exportacao atual.
  - Status: `concluida`

- [x] Fase 4 - Rollout controlado
  - Objetivo: preparar a adocao operacional do script por usuarios finais.
  - Entregaveis: documentacao de uso no `README.md`, exemplo de `.env` minimo e orientacoes de execucao em PowerShell.
  - Criterio de conclusao: um operador consegue configurar o `.env` e executar o script apenas com a documentacao.
  - Status: `concluida`

- [x] Fase 5 - Estabilizacao e fechamento
  - Objetivo: consolidar a entrega com testes finais, ajustes de nomenclatura e status atualizado.
  - Entregaveis: suite relevante verde, spec atualizada e historico preenchido com o que foi entregue.
  - Criterio de conclusao: feature concluida com implementacao validada e documentacao sincronizada com o codigo.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados:
  - teste do parser de `.env` em cenarios com comentarios, linhas em branco e chaves obrigatorias ausentes;
  - teste da composicao do nome e do destino do CSV no diretorio corrente;
  - teste do fluxo equivalente a opcao `3`, garantindo colunas e quantidade de linhas exportadas.
- Testes manuais:
  - executar o script PowerShell a partir de uma pasta temporaria e validar que o CSV foi criado nela;
  - confirmar exibicao do banner `SkyhighMonitor` e mensagens operacionais no console;
  - abrir o CSV gerado e conferir colunas `incident_id`, `from` e `to`.
- Cenarios de regressao:
  - a opcao `3` atual do menu Python continua funcionando sem alteracao de comportamento;
  - o `.env.example` do projeto permanece compativel com o fluxo Python atual;
  - a autenticacao continua respeitando o endpoint configurado sem quebrar tenants existentes.

## 7. Rollout e rollback

- Estrategia de rollout:
  - introduzir o script PowerShell como caminho adicional, sem alterar o fluxo ja existente do CLI;
  - documentar primeiro o caso minimo de uso com `.env` enxuto e execucao local em Windows PowerShell ou PowerShell 7.
- Estrategia de rollback:
  - remover o script `.ps1` e a documentacao associada caso o fluxo apresente divergencia funcional;
  - preservar a implementacao Python atual da opcao `3` como fallback operacional imediato.

## 8. Historico de atualizacoes

- 2026-03-10 - Spec criada.
- 2026-03-10 - Escopo inicial definido para extrair a opcao `3` do menu em um script PowerShell com banner, `.env` minimo e CSV gerado no diretorio atual.
- 2026-03-10 - Fases 1 a 5 concluidas com a criacao do fluxo `--export-exchange-csv`, suporte a `--env-file`, script `export-exchange-incidents.ps1` e documentacao operacional do `.env` minimo.
- 2026-03-10 - Script `export-exchange-incidents.ps1` refeito para PowerShell nativo, sem dependencia de Python, com autenticacao basic-only, paginacao, filtro Exchange Online e exportacao CSV local.

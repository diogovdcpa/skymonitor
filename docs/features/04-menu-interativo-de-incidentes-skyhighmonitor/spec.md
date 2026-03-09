# Feature 04: Menu interativo de incidentes SkyhighMonitor

- ID: `04`
- Slug: `menu-interativo-de-incidentes-skyhighmonitor`
- Criada em: 2026-03-09
- Status geral: `concluida`
- Resumo: Adicionar um menu textual no CLI com banner, consulta padrao de incidentes do dia e atalho para incidentes new de Microsoft Exchange Online com janela de dias parametrizavel.

## 1. Objetivo

Adicionar um menu textual ao CLI para reduzir a dependencia de argumentos manuais e padronizar duas consultas operacionais recorrentes.

O menu deve abrir com um banner `SkyhighMonitor` e oferecer:
- consulta de todos os incidentes com padrao no dia atual, permitindo ao usuario informar a quantidade de dias retroativos;
- consulta de incidentes filtrados por `status = new` e `service = Microsoft Exchange Online`, com padrao no dia atual e opcao de informar a quantidade de dias retroativos.

O resultado esperado e um fluxo interativo simples de executar, sem quebrar o uso atual por argumentos de linha de comando.

## 2. Contexto da codebase

- Modulos/areas impactadas:
  - `app.py` concentra autenticacao, descoberta de endpoint, consulta paginada e serializacao da resposta.
  - `README.md` documenta apenas o modo atual via argumentos/variaveis de ambiente.
  - `tests/test_env_scripts.py` cobre apenas scripts de ambiente, sem testes para o comportamento do CLI.
- Dependencias tecnicas:
  - O projeto usa apenas biblioteca padrao em runtime; a implementacao do menu deve manter essa caracteristica.
  - A configuracao continua vindo de `.env` e variaveis `SKY_*`.
  - O endpoint `queryIncidents` ja aceita `startTime` e `incidentCriteria`, o que viabiliza encapsular os filtros do menu em funcoes reutilizaveis.
- Riscos e restricoes:
  - O `app.py` hoje mistura parser de argumentos, regras de negocio e I/O; sem refatoracao minima o menu tende a aumentar o acoplamento.
  - O volume de incidentes pode ser alto; o menu precisa limitar exibicao em tela e orientar exportacao/serializacao para nao degradar usabilidade.
  - A semantica de "dia atual" depende de construir `startTime` corretamente e deixar claro que a API pode retornar incidentes antigos modificados dentro da janela consultada.
  - Pela regra do repositorio, a implementacao deve seguir TDD e so pode ser considerada concluida com testes relevantes passando na venv.

## 3. Referencias externas (opcional, recomendado)

Nenhuma referencia externa foi necessaria nesta etapa. A spec foi baseada na codebase atual e no comportamento observado da API ja integrada no projeto.

## 4. Escopo

### Em escopo

- Exibir banner textual `SkyhighMonitor` ao iniciar o modo interativo.
- Criar um menu principal com opcoes numeradas e mensagem de saida clara.
- Implementar opcao "Todos os incidentes" com padrao de `1` dia e possibilidade de o usuario informar outro numero inteiro positivo.
- Implementar opcao "Incidentes new de Microsoft Exchange Online" com padrao de `1` dia e possibilidade de o usuario informar outro numero inteiro positivo.
- Converter a quantidade de dias informada pelo usuario em `startTime` compativel com a API.
- Reaproveitar a logica existente de autenticacao, descoberta de conexao e paginacao, evitando duplicacao de fluxo HTTP.
- Extrair funcoes auxiliares para montar filtros, calcular janela de consulta e formatar a saida em tela.
- Manter compatibilidade com o modo atual por argumentos para nao quebrar automacoes existentes.
- Adicionar testes automatizados para o menu, para o calculo da janela de dias e para a montagem do filtro `new + Microsoft Exchange Online`.
- Atualizar a documentacao de uso no `README.md`.

### Fora de escopo

- Interface grafica, TUI com navegacao por setas ou dependencias externas como `prompt_toolkit`.
- Persistencia local de historico de consultas.
- Exportacao direta para CSV/TSV pelo menu nesta primeira entrega.
- Novos filtros alem dos dois fluxos solicitados.
- Alteracoes no modelo de autenticacao da Skyhigh.

## 5. Plano de implantacao (maximo 5 fases)

Atualizar durante a execucao:
- Marcar `[x]` quando a fase concluir.
- Atualizar `Status` da fase.
- Registrar no historico ao final de cada fase.

- [x] Fase 1 - Descoberta e desenho
  - Objetivo: isolar o nucleo de consulta atual em funcoes mais testaveis e definir a estrutura do menu sem alterar o comportamento existente.
  - Entregaveis: desenho do fluxo interativo, funcao para calcular `startTime` a partir de dias, funcao para montar filtros predefinidos e atualizacao da spec.
  - Criterio de conclusao: responsabilidades do menu e do fluxo legado estao separadas no desenho e cobertas por cenarios de teste planejados.
  - Status: `concluida`

- [x] Fase 2 - Implementacao base
  - Objetivo: implementar o modo interativo com banner, leitura de opcao e reaproveitamento do fluxo de consulta existente.
  - Entregaveis: entrada `--menu` ou comportamento interativo equivalente, banner `SkyhighMonitor`, menu principal, validacao da quantidade de dias e execucao da opcao "todos os incidentes".
  - Criterio de conclusao: usuario consegue abrir o menu, escolher a opcao padrao e obter incidentes do dia atual ou de uma janela informada.
  - Status: `concluida`

- [x] Fase 3 - Integracao e validacao tecnica
  - Objetivo: adicionar a opcao filtrada para `new + Microsoft Exchange Online` e validar o encadeamento completo.
  - Entregaveis: construcao do `incidentCriteria`, exibicao do resultado filtrado, testes automatizados de integracao do menu e cenarios de entrada invalida.
  - Criterio de conclusao: o menu executa ambas as consultas solicitadas e os testes cobrindo filtros e fluxo interativo passam.
  - Status: `concluida`

- [x] Fase 4 - Rollout controlado
  - Objetivo: atualizar a documentacao e validar a operacao manual no ambiente real com credenciais configuradas.
  - Entregaveis: `README.md` revisado, exemplos de execucao, checklist manual de consulta do dia atual e da consulta filtrada.
  - Criterio de conclusao: a documentacao permite reproduzir o fluxo sem leitura do codigo e a validacao manual confirma o resultado esperado.
  - Status: `concluida`

- [x] Fase 5 - Estabilizacao e fechamento
  - Objetivo: fechar a feature com limpeza de codigo, regressao validada e status atualizado.
  - Entregaveis: ajustes finais de UX textual, remocao de duplicacoes, execucao completa de testes relevantes e atualizacao do historico da spec.
  - Criterio de conclusao: implementacao concluida com testes passando e spec refletindo o estado final.
  - Status: `concluida`

## 6. Validacao

- Testes automatizados:
  - testes unitarios para calculo da janela de dias e geracao de `startTime`;
  - testes unitarios para o filtro `status = new` e `service = Microsoft Exchange Online`;
  - testes de CLI/menu simulando entrada do usuario e garantindo selecao correta da consulta;
  - testes de nao regressao para o modo legado por argumentos.
- Testes manuais:
  - abrir o menu e sair sem executar consulta;
  - executar "Todos os incidentes" com valor padrao;
  - executar "Todos os incidentes" com quantidade customizada de dias;
  - executar "Incidentes new de Microsoft Exchange Online" com valor padrao;
  - executar a mesma opcao com quantidade customizada de dias;
  - validar mensagens de erro para entradas invalidas.
- Cenarios de regressao:
  - execucao atual `python app.py --pretty` continua funcional;
  - autenticacao e descoberta automatica de endpoint permanecem inalteradas;
  - formato JSON legado continua disponivel fora do menu.

## 7. Rollout e rollback

- Estrategia de rollout:
  - introduzir o menu de forma opt-in por argumento ou fluxo claramente delimitado;
  - manter o comportamento atual por argumentos durante toda a entrega;
  - validar primeiro com consultas reais de curto intervalo antes de ampliar o uso operacional.
- Estrategia de rollback:
  - desabilitar o ponto de entrada do menu e preservar apenas o fluxo legado;
  - reverter as alteracoes em `app.py`, testes e documentacao caso a UX interativa comprometa a operacao.

## 8. Historico de atualizacoes

- 2026-03-09 - Spec criada.
- 2026-03-09 - Fase 1 concluida com desenho inicial da feature, escopo fechado e plano de implantacao definido.
- 2026-03-09 - Fases 2, 3 e 4 concluidas com implementacao do menu, testes automatizados e atualizacao do README.
- 2026-03-09 - Fase 5 concluida com estabilizacao final do CLI, ajuste de compatibilidade em `main()` e suite oficial validada com `23 passed in 0.61s`.

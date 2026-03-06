# Skyhigh - Invoke Incident API

> Nome principal: `skyhigh`
> Fonte base: `conteudo-fornecido-no-chat-2026-03-06`
> Ultima geracao: `2026-03-06` (UTC)

## Sumario

- [01 - Visao geral](./01-visao-geral.md)
- [02 - Autenticacao com Basic Auth](./02-autenticacao-com-basic-auth.md)
- [03 - Autenticacao com Access Token (IAM)](./03-autenticacao-com-access-token-iam.md)
- [04 - Consulta de Incidentes](./04-consulta-de-incidentes.md)
- [05 - Resposta da API e Campos](./05-resposta-da-api-e-campos.md)
- [06 - Troubleshooting e Boas praticas](./06-troubleshooting-e-boas-praticas.md)

## Conteudo importado

<!-- DOCUMENTA:START -->

### 01 - Visao geral

<!-- SOURCE: 01-visao-geral.md -->

## Objetivo
Documentar como consultar incidentes via API externa do Skyhigh Security, cobrindo os dois modelos de autenticacao suportados e o fluxo completo ate a consulta em `queryIncidents`.

## Conteudo
## Escopo
- API principal: `POST /shnapi/rest/external/api/v1/queryIncidents`
- Ambiente usado nos exemplos: `https://www.myshn.net`
- Ultima atualizacao da fonte: `May 23, 2025`

## Metodos de autenticacao disponiveis
1. Basic Auth
- Usa `username:password` direto na chamada de `queryIncidents`.
- Bom para integracoes simples e controladas.

2. Access Token Authentication
- Fluxo em duas etapas para obter `x-access-token`.
- Recomendado para integracoes com melhor controle de sessao/expiracao.

## Fluxo rapido (Access Token)
1. Gerar token IAM com credenciais de usuario e `bps-tenant-id`.
2. Trocar token IAM por `access_token` final no `neo-auth-service`.
3. Consultar incidentes com header `x-access-token`.

## Endpoint de consulta
- Metodo: `POST`
- Rota: `/shnapi/rest/external/api/v1/queryIncidents`
- Query string comum: `?limit=500`
- Ordenacao: crescente por ultima modificacao.

## Referencias
- Fonte base: `Invoke Incident API` (conteudo fornecido no chat)
- Secoes desta referencia:
  - `02-autenticacao-com-basic-auth.md`
  - `03-autenticacao-com-access-token-iam.md`
  - `04-consulta-de-incidentes.md`
  - `05-resposta-da-api-e-campos.md`
  - `06-troubleshooting-e-boas-praticas.md`

### 02 - Autenticacao com Basic Auth

<!-- SOURCE: 02-autenticacao-com-basic-auth.md -->

## Objetivo
Mostrar como consultar incidentes diretamente com credenciais de usuario via Basic Auth.

## Conteudo
## Quando usar
- Integracoes internas simples.
- Cenarios em que o gerenciamento de token separado nao e necessario.

## Requisitos
- Usuario com permissao no tenant.
- Senha valida.
- Endpoint acessivel (`www.myshn.net`).

## Exemplo de chamada
```bash
curl -u '<username>:<password>' \
  -H 'Content-Type: application/json' \
  'https://www.myshn.net/shnapi/rest/external/api/v1/queryIncidents?limit=500' \
  -d '{
    "startTime": "2020-04-12T09:30:00.000",
    "incidentCriteria": {
      "categories": [
        { "incidentType": "Alert.Policy.Epo" }
      ]
    }
  }'
```

## Parametros usados
- `startTime`: inicio da janela de busca.
- `incidentCriteria.categories[].incidentType`: tipo/categoria de incidente.
- `limit` (query param): quantidade maxima de registros por chamada.

## Observacoes operacionais
- Use cofres de segredo para armazenar credenciais.
- Nunca registre `username:password` em logs.
- Prefira HTTPS sempre (obrigatorio em producao).

## Referencias
- Endpoint: `POST /v1/queryIncidents`
- Fonte base: `Invoke Incident API`

### 03 - Autenticacao com Access Token (IAM)

<!-- SOURCE: 03-autenticacao-com-access-token-iam.md -->

## Objetivo
Documentar o fluxo de autenticacao em duas etapas para obter `x-access-token` e usar na consulta de incidentes.

## Conteudo
## Visao do fluxo
1. Solicitar token IAM com `grant_type=password` e `token_type=iam`.
2. Trocar o IAM token por `access_token` no `neo-auth-service`.
3. Usar `x-access-token` na chamada de `queryIncidents`.

## Passo 1: obter token IAM
```bash
curl --location --request POST \
  'https://www.myshn.net/shnapi/rest/external/api/v1/token?grant_type=password&token_type=iam' \
  --header 'bps-tenant-id: <BPSTenantId>' \
  --header 'Authorization: Basic <BASE64_CREDENTIALS>'
```

Resposta esperada (exemplo):
```json
{
  "access_token": "<iam_token>",
  "token_type": "bearer"
}
```

## Passo 2: obter access token final
```bash
curl --location \
  'https://www.myshn.net/neo/neo-auth-service/oauth/token?grant_type=iam_token&skip_audit=true' \
  --header 'x-iam-token: <Token gerado no passo 1>' \
  --header 'Content-Type: application/json' \
  --data '{}'
```

Resposta esperada (exemplo):
```json
{
  "access_token": "<access_token_final>",
  "token_type": "bearer",
  "refresh_token": "<refresh_token>",
  "expires_in": 899,
  "scope": "read write"
}
```

## Pontos importantes
- O header `bps-tenant-id` e obrigatorio quando ha multiplos tenants.
- O `access_token` expira (`expires_in`), entao a integracao deve renovar quando necessario.
- Trate tokens como segredos: nao salvar em texto puro.

## Referencias
- Endpoints:
  - `POST /shnapi/rest/external/api/v1/token?grant_type=password&token_type=iam`
  - `POST /neo/neo-auth-service/oauth/token?grant_type=iam_token&skip_audit=true`
- Fonte base: `Invoke Incident API`

### 04 - Consulta de Incidentes

<!-- SOURCE: 04-consulta-de-incidentes.md -->

## Objetivo
Padronizar como montar e executar a consulta de incidentes apos autenticacao.

## Conteudo
## Endpoint
- Metodo: `POST`
- URL: `https://www.myshn.net/shnapi/rest/external/api/v1/queryIncidents?limit=500`

## Exemplo com access token
```bash
curl --location \
  'https://www.myshn.net/shnapi/rest/external/api/v1/queryIncidents?limit=500' \
  --header 'x-access-token: <Token do passo 2>' \
  --header 'Content-Type: application/json' \
  --data '{
    "startTime": "2025-04-01T00:00:00Z",
    "endTime": "2025-04-03T00:00:00Z",
    "incidentCriteria": {
      "categories": [
        { "incidentType": "Alert.Policy" }
      ]
    }
  }'
```

## Parametros de filtro
- `startTime`: inicio do periodo.
- `endTime`: fim do periodo.
- `incidentCriteria.categories[].incidentType`: filtro por tipo de incidente.
- `limit`: pagina/logica de lote por requisicao.

## Estrategia recomendada para paginacao temporal
1. Use uma janela inicial (`startTime`/`endTime`) controlada.
2. Leia `responseInfo.nextStartTime` na resposta.
3. Na proxima chamada, reutilize `nextStartTime` para continuar sem lacunas.

## Boas praticas
- Padronize timezone em UTC (`Z`).
- Comece com `limit` menor em testes.
- Implemente retry com backoff para falhas transientes.

## Referencias
- Endpoint: `POST /v1/queryIncidents`
- Fonte base: `Invoke Incident API`

### 05 - Resposta da API e Campos

<!-- SOURCE: 05-resposta-da-api-e-campos.md -->

## Objetivo
Explicar o formato da resposta da API de incidentes e os campos mais relevantes para ingestao/analytics.

## Conteudo
## Status de sucesso
- HTTP: `200 OK`
- A lista de incidentes vem em `body.incidents`.
- Metadados da consulta ficam em `body.responseInfo`.

## Estrutura geral (resumida)
```json
{
  "body": {
    "responseInfo": {
      "actualLimit": 2,
      "apiElapsedMillis": 571,
      "nextStartTime": "2025-04-01T07:20:52.478Z"
    },
    "incidents": [
      {
        "incidentId": "DLP-89265",
        "incidentGroup": "Alert.Policy.Dlp",
        "incidentRiskSeverity": "low",
        "status": "new",
        "timeCreated": "2025-04-01T07:20:17.000Z",
        "timeModified": "2025-04-01T07:20:37.811Z",
        "information": {
          "policyName": "OF-2288",
          "contentItemName": "Confidential.docx",
          "source": "API"
        }
      }
    ]
  },
  "statusCodeValue": 200,
  "statusCode": "OK"
}
```

## Campos-chave para integracao
- `incidentId`: identificador unico de incidente.
- `incidentGroup` / `incidentGroupId`: agrupamento e tipologia.
- `incidentRiskScore` / `incidentRiskSeverity`: risco numerico e categorico.
- `status`: estado atual (ex.: `new`).
- `timeCreated`, `timeModified`, `significantlyUpdatedAt`: controle temporal.
- `information.*`: contexto de arquivo, politica, fonte, colaboracao e device.

## Campos de controle de coleta
- `responseInfo.actualLimit`: quantidade real retornada.
- `responseInfo.nextStartTime`: cursor temporal para continuar coleta.
- `responseInfo.error`: erro retornado pela API quando houver.

## Referencias
- Fonte base: `Invoke Incident API`
- Endpoint de consulta: `POST /v1/queryIncidents`

### 06 - Troubleshooting e Boas praticas

<!-- SOURCE: 06-troubleshooting-e-boas-praticas.md -->

## Objetivo
Listar falhas comuns de autenticacao/consulta e um checklist de robustez para operacao continua.

## Conteudo
## Problemas comuns e validacoes
1. `401/403` na autenticacao
- Validar `Authorization` (Basic), usuario/senha e permissao no tenant.
- No fluxo IAM, validar `bps-tenant-id` correto.

2. `401` no `queryIncidents` com token
- Confirmar que o token e do passo 2 (`access_token` final).
- Verificar expiracao (`expires_in`) e renovar token.

3. Sem resultados
- Revisar janela `startTime`/`endTime`.
- Revisar filtro `incidentType`.
- Testar sem filtro de categoria para diagnostico.

4. Erro de formato de payload
- Garantir `Content-Type: application/json`.
- Validar JSON e nomes de campos esperados.

## Checklist de producao
- Segredos em cofre (nao em codigo/repositorio).
- Rotacao de credenciais e tokens.
- Logs sem dados sensiveis.
- Retentativa com backoff e limite de tentativas.
- Alertas para falhas consecutivas e latencia alta.
- Monitorar `apiElapsedMillis` e volume de incidentes.

## Modelo de rotina de coleta
1. Renovar token (quando necessario).
2. Consultar incidentes por janela.
3. Persistir incidente e cursor (`nextStartTime`).
4. Repetir ciclo com idempotencia.

## Referencias
- Fonte base: `Invoke Incident API`
- Suporte de tenant/BPS ID: Skyhigh Security Support

<!-- DOCUMENTA:END -->

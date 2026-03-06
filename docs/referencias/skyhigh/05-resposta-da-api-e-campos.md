# 05 - Resposta da API e Campos

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

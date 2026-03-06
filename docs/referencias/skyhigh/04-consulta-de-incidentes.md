# 04 - Consulta de Incidentes

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

# 02 - Autenticacao com Basic Auth

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

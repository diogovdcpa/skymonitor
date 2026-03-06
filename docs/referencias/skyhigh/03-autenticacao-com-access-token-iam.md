# 03 - Autenticacao com Access Token (IAM)

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

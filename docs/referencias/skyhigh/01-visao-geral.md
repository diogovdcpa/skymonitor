# 01 - Visao geral

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

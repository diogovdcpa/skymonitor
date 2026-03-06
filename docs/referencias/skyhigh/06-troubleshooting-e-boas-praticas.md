# 06 - Troubleshooting e Boas praticas

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

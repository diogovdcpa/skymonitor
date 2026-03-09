#!/usr/bin/env bash

if ! (return 0 2>/dev/null); then
  echo "Erro: execute com 'source env-script/stop.sh'." >&2
  exit 1
fi

if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "Nenhum ambiente virtual ativo." >&2
  return 0
fi

if ! command -v deactivate >/dev/null 2>&1; then
  echo "Erro: a funcao 'deactivate' nao esta disponivel nesta sessao." >&2
  return 1
fi

deactivate
echo "Ambiente virtual encerrado."

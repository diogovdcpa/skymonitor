#!/usr/bin/env bash

if ! (return 0 2>/dev/null); then
  echo "Erro: execute com 'source env-script/start.sh'." >&2
  exit 1
fi

if [ ! -f ".venv/bin/activate" ]; then
  echo "Erro: arquivo .venv/bin/activate nao encontrado." >&2
  return 1
fi

# shellcheck disable=SC1091
source ".venv/bin/activate"
test -n "${VIRTUAL_ENV:-}" || {
  echo "Erro: ative um ambiente virtual antes de executar comandos." >&2
  return 1
}

echo "Ambiente virtual ativo: ${VIRTUAL_ENV}"

#!/usr/bin/env bash
set -euo pipefail

test -n "${VIRTUAL_ENV:-}" || {
  echo "Erro: ative um ambiente virtual antes de executar comandos."
  exit 1
}

python -m ruff check "$@"

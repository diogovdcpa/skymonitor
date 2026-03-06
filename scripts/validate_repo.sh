#!/usr/bin/env bash
set -euo pipefail

echo "Validando estrutura minima do repositorio..."

test -f README.md
test -f CONTRIBUTING.md
test -f .github/pull_request_template.md

skill_files_count="$(find skills -type f -name 'SKILL.md' | wc -l | tr -d ' ')"
if [ "${skill_files_count}" -lt 1 ]; then
  echo "Nenhum SKILL.md encontrado em skills/"
  exit 1
fi

echo "Validando frontmatter basico dos SKILL.md..."
while IFS= read -r skill_file; do
  grep -q '^---$' "$skill_file"
  grep -q '^name:' "$skill_file"
  grep -q '^description:' "$skill_file"
done < <(find skills -type f -name 'SKILL.md' | sort)

echo "Validacao concluida com sucesso."

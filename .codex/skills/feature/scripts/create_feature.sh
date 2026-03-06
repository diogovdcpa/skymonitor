#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat << 'USAGE'
Usage:
  bash .codex/skills/feature/scripts/create_feature.sh "Nome da Feature" "Resumo opcional"
USAGE
}

if [ $# -lt 1 ]; then
  usage
  exit 1
fi

feature_name="$1"
summary="${2:-Descrever o objetivo da feature em 1-2 frases.}"

slug="$(printf '%s' "$feature_name" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"

if [ -z "$slug" ]; then
  echo "Erro: nao foi possivel gerar slug para o nome da feature: $feature_name" >&2
  exit 1
fi

if git rev-parse --show-toplevel >/dev/null 2>&1; then
  repo_root="$(git rev-parse --show-toplevel)"
else
  repo_root="$(pwd)"
fi
features_dir="$repo_root/docs/features"
template_file="$(cd "$(dirname "$0")/.." && pwd)/references/spec-template.md"

if [ ! -f "$template_file" ]; then
  echo "Erro: template nao encontrado em $template_file" >&2
  exit 1
fi

mkdir -p "$features_dir"

last_number="$(find "$features_dir" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sed -nE 's/^([0-9]{2})-.*/\1/p' | sort -n | tail -n 1)"

if [ -z "$last_number" ]; then
  next_number=1
else
  next_number=$((10#$last_number + 1))
fi

printf -v feature_id "%02d" "$next_number"
feature_dir="$features_dir/$feature_id-$slug"
spec_file="$feature_dir/spec.md"

if [ -e "$feature_dir" ]; then
  echo "Erro: diretorio ja existe: $feature_dir" >&2
  exit 1
fi

mkdir -p "$feature_dir"

today="$(date -u +%Y-%m-%d)"

escape_sed() {
  printf '%s' "$1" | sed -e 's/[\/&]/\\&/g'
}

sed \
  -e "s/__FEATURE_ID__/$(escape_sed "$feature_id")/g" \
  -e "s/__FEATURE_NAME__/$(escape_sed "$feature_name")/g" \
  -e "s/__FEATURE_SLUG__/$(escape_sed "$slug")/g" \
  -e "s/__DATE__/$(escape_sed "$today")/g" \
  -e "s/__SUMMARY__/$(escape_sed "$summary")/g" \
  "$template_file" > "$spec_file"

echo "Feature criada: $feature_dir"
echo "Spec criada: $spec_file"

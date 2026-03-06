#!/usr/bin/env python3
"""
Create and maintain reference markdown docs in docs/referencias/<name>/.

Behavior:
- Create section files NN-topic.md when missing.
- Regenerate index.md with:
  - section summary
  - consolidated imported content from all section files
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import unicodedata
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


DEFAULT_SECTIONS = [
    "Visao geral",
    "Conceitos chave",
    "Configuracao",
    "Operacao",
    "Troubleshooting",
]


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    return slug or "referencia"


def remove_main_heading(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return text.strip()


def read_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


def ensure_section_file(path: Path, index: int, title: str) -> None:
    if path.exists():
        return
    content = (
        f"# {index:02d} - {title}\n\n"
        "## Objetivo\n"
        "[TODO: Escrever objetivo da secao]\n\n"
        "## Conteudo\n"
        "[TODO: Escrever conteudo baseado no arquivo fonte]\n\n"
        "## Referencias\n"
        "- [TODO]\n"
    )
    path.write_text(content, encoding="utf-8")


def discover_section_files(target_dir: Path) -> List[Path]:
    return sorted(
        p
        for p in target_dir.iterdir()
        if p.is_file() and re.match(r"^\d{2}-.+\.md$", p.name)
    )


def build_summary(section_data: Sequence[Tuple[Path, str]]) -> str:
    lines = [f"- [{title}](./{path.name})" for path, title in section_data]
    return "\n".join(lines) if lines else "- [Sem secoes](#conteudo-importado)"


def build_import_block(section_data: Sequence[Tuple[Path, str]]) -> str:
    if not section_data:
        return "_Nenhuma secao encontrada._"

    blocks: List[str] = []
    for path, title in section_data:
        raw = path.read_text(encoding="utf-8")
        body = remove_main_heading(raw)
        section_body = body if body else "_Sem conteudo._"
        blocks.append(
            f"### {title}\n\n"
            f"<!-- SOURCE: {path.name} -->\n\n"
            f"{section_body}\n"
        )
    return "\n".join(blocks).rstrip()


def build_index_content(
    *,
    doc_title: str,
    doc_name: str,
    source: str | None,
    section_data: Sequence[Tuple[Path, str]],
) -> str:
    generated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    source_line = source if source else "nao informado"
    summary = build_summary(section_data)
    imported = build_import_block(section_data)
    return (
        f"# {doc_title}\n\n"
        f"> Nome principal: `{doc_name}`\n"
        f"> Fonte base: `{source_line}`\n"
        f"> Ultima geracao: `{generated_at}` (UTC)\n\n"
        "## Sumario\n\n"
        f"{summary}\n\n"
        "## Conteudo importado\n\n"
        "<!-- DOCUMENTA:START -->\n\n"
        f"{imported}\n\n"
        "<!-- DOCUMENTA:END -->\n"
    )


def collect_section_data(section_files: Iterable[Path]) -> List[Tuple[Path, str]]:
    data: List[Tuple[Path, str]] = []
    for path in section_files:
        text = path.read_text(encoding="utf-8")
        fallback = path.stem.replace("-", " ")
        title = read_title(text, fallback)
        data.append((path, title))
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create markdown documentation structure under docs/referencias/<name>/."
    )
    parser.add_argument("--name", required=True, help="Main reference name, e.g. fortinet")
    parser.add_argument("--source", help="Path or label of source file used for this documentation")
    parser.add_argument(
        "--section",
        action="append",
        default=[],
        help="Section title. Can be repeated. If omitted, uses existing section files or defaults.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root where docs/referencias will be created (default: current dir).",
    )
    parser.add_argument(
        "--title",
        help="Document title shown in index.md. Default: capitalized name.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    doc_name_slug = slugify(args.name)
    doc_title = args.title.strip() if args.title else args.name.strip().title()

    target_dir = root / "docs" / "referencias" / doc_name_slug
    target_dir.mkdir(parents=True, exist_ok=True)

    requested_sections = [s.strip() for s in args.section if s and s.strip()]
    if requested_sections:
        for idx, section_title in enumerate(requested_sections, start=1):
            file_name = f"{idx:02d}-{slugify(section_title)}.md"
            ensure_section_file(target_dir / file_name, idx, section_title)

    section_files = discover_section_files(target_dir)
    if not section_files:
        for idx, section_title in enumerate(DEFAULT_SECTIONS, start=1):
            file_name = f"{idx:02d}-{slugify(section_title)}.md"
            ensure_section_file(target_dir / file_name, idx, section_title)
        section_files = discover_section_files(target_dir)

    section_data = collect_section_data(section_files)
    index_content = build_index_content(
        doc_title=doc_title,
        doc_name=doc_name_slug,
        source=args.source,
        section_data=section_data,
    )

    index_path = target_dir / "index.md"
    index_path.write_text(index_content, encoding="utf-8")

    print(f"[OK] Pasta: {target_dir}")
    print(f"[OK] Principal: {index_path}")
    for path, _ in section_data:
        print(f"[OK] Secao: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

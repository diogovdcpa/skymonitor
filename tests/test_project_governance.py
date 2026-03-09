from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_declares_pytest_and_ruff_configuration() -> None:
    pyproject_path = REPO_ROOT / "pyproject.toml"

    assert pyproject_path.exists(), "pyproject.toml deve existir para centralizar a configuracao."

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    assert data["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]
    assert data["tool"]["ruff"]["line-length"] == 100
    assert data["tool"]["ruff"]["extend-exclude"] == [".codex"]
    assert data["tool"]["ruff"]["lint"]["select"] == ["E", "F", "I", "B"]
    assert data["tool"]["mypy"]["files"] == [
        "skymonitor/config.py",
        "skymonitor/types.py",
        "skymonitor/api.py",
        "skymonitor/cli.py",
    ]
    assert data["tool"]["mypy"]["strict"] is True


def test_readme_mentions_current_test_suites() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "tests/test_app_business_rules.py" in readme
    assert "tests/test_app_menu.py" in readme
    assert "tests/test_env_scripts.py" in readme
    assert "cobre apenas os scripts de ambiente" not in readme


def test_reference_index_keeps_only_one_h1_and_no_duplicate_conteudo_heading() -> None:
    index_path = REPO_ROOT / "docs" / "referencias" / "skyhigh" / "index.md"
    content = index_path.read_text(encoding="utf-8")

    h1_count = sum(1 for line in content.splitlines() if line.startswith("# "))
    assert h1_count == 1
    assert "## Conteudo\n## " not in content


def test_modularized_package_files_exist() -> None:
    assert (REPO_ROOT / "skymonitor" / "__init__.py").exists()
    assert (REPO_ROOT / "skymonitor" / "api.py").exists()
    assert (REPO_ROOT / "skymonitor" / "cli.py").exists()


def test_legacy_app_module_reuses_package_main() -> None:
    app_module = importlib.import_module("app")
    cli_module = importlib.import_module("skymonitor.cli")

    assert app_module.main is cli_module.main

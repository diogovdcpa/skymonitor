from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_shell(command: str, *, activate_venv: bool = False) -> subprocess.CompletedProcess[str]:
    prefix = ""
    if activate_venv:
        prefix = "source .venv/bin/activate\n"

    return subprocess.run(
        ["bash", "-lc", prefix + command],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        env=os.environ.copy(),
    )


def test_start_script_requires_source_invocation() -> None:
    result = run_shell("bash env-script/start.sh")

    assert result.returncode != 0
    assert "source env-script/start.sh" in result.stderr


def test_start_script_exports_virtual_env_when_sourced() -> None:
    result = run_shell('source env-script/start.sh >/dev/null && printf "%s" "$VIRTUAL_ENV"')

    assert result.returncode == 0
    assert result.stdout.strip().endswith("/.venv")


def test_stop_script_requires_source_invocation() -> None:
    result = run_shell("bash env-script/stop.sh")

    assert result.returncode != 0
    assert "source env-script/stop.sh" in result.stderr


def test_stop_script_deactivates_virtual_env_when_sourced() -> None:
    result = run_shell(
        """
        source .venv/bin/activate
        source env-script/stop.sh >/dev/null
        if [ -n "${VIRTUAL_ENV:-}" ]; then
          printf "active"
        fi
        """
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_test_script_requires_active_virtual_env() -> None:
    result = run_shell("unset VIRTUAL_ENV\nbash env-script/test.sh")

    assert result.returncode != 0
    assert "Erro: ative um ambiente virtual antes de executar comandos." in result.stdout


def test_test_script_runs_pytest_quiet_mode() -> None:
    result = run_shell(
        (
            "bash env-script/test.sh tests/test_env_scripts.py "
            "-k test_start_script_requires_source_invocation"
        ),
        activate_venv=True,
    )

    assert result.returncode == 0
    assert "[100%]" in result.stdout
    assert "collected " not in result.stdout


def test_lint_script_requires_active_virtual_env() -> None:
    result = run_shell("unset VIRTUAL_ENV\nbash env-script/lint.sh")

    assert result.returncode != 0
    assert "Erro: ative um ambiente virtual antes de executar comandos." in result.stdout


def test_lint_script_runs_ruff_check() -> None:
    result = run_shell("bash env-script/lint.sh tests/test_env_scripts.py", activate_venv=True)

    assert result.returncode == 0
    assert "All checks passed!" in result.stdout


def test_typecheck_script_requires_active_virtual_env() -> None:
    result = run_shell("unset VIRTUAL_ENV\nbash env-script/typecheck.sh")

    assert result.returncode != 0
    assert "Erro: ative um ambiente virtual antes de executar comandos." in result.stdout


def test_typecheck_script_runs_mypy() -> None:
    result = run_shell(
        "bash env-script/typecheck.sh skymonitor/config.py skymonitor/types.py",
        activate_venv=True,
    )

    assert result.returncode == 0
    assert "Success: no issues found" in result.stdout

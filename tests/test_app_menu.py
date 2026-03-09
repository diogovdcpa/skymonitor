from __future__ import annotations

import argparse
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

import pytest

import app
from skymonitor import cli as cli_module


def test_build_start_time_for_days_uses_current_day_midnight() -> None:
    now = datetime(2026, 3, 9, 15, 47, 12)

    assert app.build_start_time_for_days(1, now=now) == "2026-03-09T00:00:00.000Z"


def test_build_start_time_for_days_supports_multiple_days() -> None:
    now = datetime(2026, 3, 9, 15, 47, 12)

    assert app.build_start_time_for_days(3, now=now) == "2026-03-07T00:00:00.000Z"


def test_build_start_time_for_days_requires_positive_value() -> None:
    with pytest.raises(ValueError, match="maior ou igual a 1"):
        app.build_start_time_for_days(0, now=datetime(2026, 3, 9, 15, 47, 12))


def test_filter_new_exchange_online_incidents_returns_only_matching_items() -> None:
    incidents = [
        {
            "incidentId": "DLP-1",
            "status": "new",
            "serviceNames": ["Microsoft Exchange Online"],
        },
        {
            "incidentId": "DLP-2",
            "status": "suppressed",
            "serviceNames": ["Microsoft Exchange Online"],
        },
        {
            "incidentId": "DLP-3",
            "status": "new",
            "serviceNames": ["OneDrive"],
        },
    ]

    filtered = app.filter_new_exchange_online_incidents(incidents)

    assert filtered == [incidents[0]]


def test_parse_args_accepts_menu_flag() -> None:
    args = app.parse_args(["--menu"])

    assert args.menu is True


def test_format_incident_line_includes_main_fields() -> None:
    line = app._format_incident_line(
        {
            "incidentId": "DLP-99",
            "incidentRiskSeverity": "HIGH",
            "status": "new",
            "actorId": "user@example.com",
            "information": {
                "contentItemName": "arquivo.xlsx",
                "policyName": "Regra Exchange",
            },
        }
    )

    assert "DLP-99" in line
    assert "severity=HIGH" in line
    assert "actor=user@example.com" in line
    assert "arquivo=arquivo.xlsx" in line
    assert "policy=Regra Exchange" in line


def test_run_menu_executes_all_incidents_option_with_default_day() -> None:
    captured: list[tuple[str, list[dict[str, str]]]] = []
    outputs: list[str] = []
    answers = iter(["1", "", "0"])

    def fake_execute(mode: str, start_time: str) -> list[dict[str, str]]:
        captured.append((mode, start_time))
        return [{"incidentId": "DLP-10"}]

    result = app.run_interactive_menu(
        input_func=lambda _: next(answers),
        output_func=outputs.append,
        execute_query=fake_execute,
        now=datetime(2026, 3, 9, 15, 47, 12),
    )

    assert result == 0
    assert captured == [("all", "2026-03-09T00:00:00.000Z")]
    assert any("SkyhighMonitor" in line for line in outputs)
    assert any("Total de incidentes retornados: 1" in line for line in outputs)


def test_run_menu_executes_exchange_option_with_custom_days() -> None:
    captured: list[tuple[str, list[dict[str, str]]]] = []
    outputs: list[str] = []
    answers = iter(["2", "3", "0"])

    def fake_execute(mode: str, start_time: str) -> list[dict[str, str]]:
        captured.append((mode, start_time))
        return [{"incidentId": "DLP-20", "status": "new"}]

    result = app.run_interactive_menu(
        input_func=lambda _: next(answers),
        output_func=outputs.append,
        execute_query=fake_execute,
        now=datetime(2026, 3, 9, 15, 47, 12),
    )

    assert result == 0
    assert captured == [("exchange_new", "2026-03-07T00:00:00.000Z")]
    assert any("Total de incidentes retornados: 1" in line for line in outputs)


def test_run_menu_reprompts_for_invalid_days() -> None:
    captured: list[tuple[str, str]] = []
    outputs: list[str] = []
    answers = iter(["1", "abc", "2", "0"])

    def fake_execute(mode: str, start_time: str) -> list[dict[str, str]]:
        captured.append((mode, start_time))
        return []

    result = app.run_interactive_menu(
        input_func=lambda _: next(answers),
        output_func=outputs.append,
        execute_query=fake_execute,
        now=datetime(2026, 3, 9, 15, 47, 12),
    )

    assert result == 0
    assert captured == [("all", "2026-03-08T00:00:00.000Z")]
    assert any("Informe um numero inteiro maior ou igual a 1." in line for line in outputs)


def test_execute_menu_query_filters_exchange_new(monkeypatch: pytest.MonkeyPatch) -> None:
    args = argparse.Namespace(
        base_url=None,
        email="user@example.com",
        password="secret",
        tenant_id=None,
        auth_path=None,
        incidents_path=None,
        start_time="2020-01-01T00:00:00.000",
        incident_criteria_json="",
        page_size=50,
        max_pages=3,
        pretty=False,
        auth_mode="basic-only",
        menu=True,
    )

    monkeypatch.setattr(
        cli_module,
        "try_resolve_connection",
        lambda **_: {
            "base_url": "https://unit.test",
            "incidents_path": "/incidents",
            "token": None,
        },
    )
    monkeypatch.setattr(
        cli_module,
        "fetch_all_incidents",
        lambda **_: [
            {
                "incidentId": "DLP-1",
                "status": "new",
                "serviceNames": ["Microsoft Exchange Online"],
            },
            {
                "incidentId": "DLP-2",
                "status": "suppressed",
                "serviceNames": ["Microsoft Exchange Online"],
            },
        ],
    )

    incidents = app.execute_menu_query(args, "exchange_new", "2026-03-09T00:00:00.000Z")

    assert incidents == [
        {"incidentId": "DLP-1", "status": "new", "serviceNames": ["Microsoft Exchange Online"]}
    ]


def test_main_opens_menu_by_default_without_cli_args() -> None:
    args = SimpleNamespace(
        base_url=None,
        email="user@example.com",
        password="secret",
        tenant_id=None,
        auth_path=None,
        incidents_path=None,
        start_time="2026-03-09T00:00:00.000",
        incident_criteria_json="",
        page_size=100,
        max_pages=10,
        pretty=False,
        auth_mode="basic-only",
        menu=False,
    )

    with (
        patch.object(cli_module, "load_dotenv"),
        patch.object(cli_module, "parse_args", return_value=args),
        patch.object(cli_module, "run_interactive_menu", return_value=0) as menu_mock,
        patch.object(cli_module, "run_standard_cli", return_value=0) as standard_mock,
        patch("sys.argv", ["app.py"]),
    ):
        exit_code = app.main()

    assert exit_code == 0
    menu_mock.assert_called_once_with(args=args)
    standard_mock.assert_not_called()


def test_main_keeps_standard_cli_when_explicit_args_are_provided() -> None:
    args = SimpleNamespace(
        base_url=None,
        email="user@example.com",
        password="secret",
        tenant_id=None,
        auth_path=None,
        incidents_path=None,
        start_time="2026-03-09T00:00:00.000",
        incident_criteria_json="",
        page_size=100,
        max_pages=10,
        pretty=True,
        auth_mode="basic-only",
        menu=False,
    )

    with (
        patch.object(cli_module, "load_dotenv"),
        patch.object(cli_module, "parse_args", return_value=args),
        patch.object(cli_module, "run_interactive_menu", return_value=0) as menu_mock,
        patch.object(cli_module, "run_standard_cli", return_value=0) as standard_mock,
        patch("sys.argv", ["app.py", "--pretty"]),
    ):
        exit_code = app.main()

    assert exit_code == 0
    menu_mock.assert_not_called()
    standard_mock.assert_called_once_with(args)

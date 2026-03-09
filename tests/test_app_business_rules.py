from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

import app
from skymonitor import api as api_module
from skymonitor import cli as cli_module


def test_extract_token_accepts_nested_data_token() -> None:
    payload = {"data": {"token": "abc123"}}

    assert app._extract_token(payload) == "abc123"


def test_extract_incident_items_reads_nested_body_incidents() -> None:
    response = {"body": {"incidents": [{"id": "1", "severity": "HIGH"}, {"id": "2"}]}}

    assert app._extract_incident_items(response) == [{"id": "1", "severity": "HIGH"}, {"id": "2"}]


def test_extract_incident_items_accepts_single_incident_object() -> None:
    response = {"id": "1", "severity": "HIGH", "status": "new"}

    assert app._extract_incident_items(response) == [response]


def test_extract_next_start_time_reads_nested_response_info() -> None:
    response = {"body": {"responseInfo": {"nextStartTime": "2026-03-09T10:00:00.000"}}}

    assert app._extract_next_start_time(response) == "2026-03-09T10:00:00.000"


def test_fetch_all_incidents_uses_next_start_time_until_last_page() -> None:
    responses = [
        {
            "incidents": [{"id": "1"}, {"id": "2"}],
            "responseInfo": {"nextStartTime": "next-token"},
        },
        {
            "incidents": [{"id": "3"}],
            "responseInfo": {"nextStartTime": "ignored"},
        },
    ]
    calls: list[str | None] = []

    def fake_query_incidents_page(**kwargs: object) -> object:
        calls.append(kwargs["start_time"])  # type: ignore[index]
        return responses[len(calls) - 1]

    with patch.object(api_module, "query_incidents_page", side_effect=fake_query_incidents_page):
        incidents = app.fetch_all_incidents(
            base_url="https://example.test",
            incidents_path="/incidents",
            page_size=2,
            max_pages=5,
            start_time="initial-token",
            incident_criteria={"severity": "HIGH"},
            token="token-123",
            email="user@example.com",
            password="secret",
        )

    assert incidents == [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    assert calls == ["initial-token", "next-token"]


def test_try_resolve_connection_returns_first_working_incidents_path() -> None:
    with (
        patch.object(api_module, "authenticate_skyhigh", return_value="token-123") as auth_mock,
        patch.object(
            api_module,
            "query_incidents_page",
            side_effect=[RuntimeError("primeiro endpoint falhou"), {"incidents": [{"id": "1"}]}],
        ) as query_mock,
    ):
        resolved = app.try_resolve_connection(
            base_candidates=["https://example.test"],
            auth_paths=["/auth/login"],
            incidents_paths=["/broken", "/working"],
            email="user@example.com",
            password="secret",
            auth_mode="skyhigh",
            page_size=100,
            start_time="2026-03-09T00:00:00.000",
            incident_criteria={"severity": "HIGH"},
            tenant_id=None,
        )

    assert resolved == {
        "base_url": "https://example.test",
        "token": "token-123",
        "incidents_path": "/working",
    }
    auth_mock.assert_called_once_with("https://example.test", "user@example.com", "secret")
    assert query_mock.call_count == 2


def test_try_resolve_connection_does_not_fallback_to_basic_in_iam_tenant_mode() -> None:
    with (
        patch.object(
            api_module, "authenticate_iam_tenant", side_effect=RuntimeError("tenant auth falhou")
        ),
        patch.object(api_module, "query_incidents_page") as query_mock,
    ):
        with pytest.raises(RuntimeError, match="Nenhuma combinacao base/auth funcionou"):
            app.try_resolve_connection(
                base_candidates=["https://example.test"],
                auth_paths=["/auth/login"],
                incidents_paths=["/incidents"],
                email="user@example.com",
                password="secret",
                auth_mode="iam-tenant",
                page_size=100,
                start_time="2026-03-09T00:00:00.000",
                incident_criteria=None,
                tenant_id="tenant-1",
            )

    query_mock.assert_not_called()


def test_main_returns_error_when_incident_criteria_is_not_an_object(
    capsys: pytest.CaptureFixture[str],
) -> None:
    args = SimpleNamespace(
        base_url=None,
        email="user@example.com",
        password="secret",
        tenant_id=None,
        auth_path=None,
        incidents_path=None,
        start_time="2026-03-09T00:00:00.000",
        incident_criteria_json=json.dumps(["invalid"]),
        page_size=100,
        max_pages=10,
        pretty=False,
        auth_mode="basic-only",
    )

    with patch.object(cli_module, "load_dotenv"), patch.object(
        cli_module, "parse_args", return_value=args
    ):
        exit_code = app.main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "--incident-criteria-json deve ser um objeto JSON." in captured.err


def test_main_requires_tenant_id_for_iam_tenant_mode(capsys: pytest.CaptureFixture[str]) -> None:
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
        auth_mode="iam-tenant",
    )

    with patch.object(cli_module, "load_dotenv"), patch.object(
        cli_module, "parse_args", return_value=args
    ):
        exit_code = app.main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Informe --tenant-id ou SKY_TENANT_ID para auth-mode iam-tenant." in captured.err

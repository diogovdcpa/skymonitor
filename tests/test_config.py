from __future__ import annotations

import argparse

import pytest

from skymonitor import config


def test_normalize_start_time_adds_utc_suffix_for_naive_timestamp() -> None:
    assert config.normalize_start_time("2026-03-09T00:00:00.000") == "2026-03-09T00:00:00.000Z"


def test_normalize_start_time_converts_offset_to_utc() -> None:
    assert config.normalize_start_time("2026-03-09T03:00:00-03:00") == "2026-03-09T06:00:00.000Z"


def test_build_runtime_config_applies_defaults_and_normalizes_start_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SKY_EMAIL", "user@example.com")
    monkeypatch.setenv("SKY_PASSWORD", "secret")
    monkeypatch.setenv("SKY_AUTH_MODE", "basic-only")

    args = argparse.Namespace(
        base_url=None,
        email=None,
        password=None,
        tenant_id=None,
        auth_path=None,
        incidents_path=None,
        start_time="2026-03-09T00:00:00",
        incident_criteria_json=None,
        page_size=None,
        max_pages=None,
        pretty=False,
        auth_mode=None,
        menu=False,
    )

    resolved = config.build_runtime_config(args)

    assert resolved.email == "user@example.com"
    assert resolved.password == "secret"
    assert resolved.page_size == 200
    assert resolved.max_pages == 1000
    assert resolved.auth_mode == "basic-only"
    assert resolved.start_time == "2026-03-09T00:00:00.000Z"

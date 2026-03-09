from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import UTC, datetime

DEFAULT_START_TIME = "2020-04-12T09:30:00.000Z"
DEFAULT_PAGE_SIZE = 200
DEFAULT_MAX_PAGES = 1000
DEFAULT_AUTH_MODE = "basic-only"


@dataclass(frozen=True)
class RuntimeConfig:
    base_url: str | None
    email: str | None
    password: str | None
    tenant_id: str | None
    auth_path: str | None
    incidents_path: str | None
    start_time: str
    incident_criteria_json: str
    page_size: int
    max_pages: int
    pretty: bool
    auth_mode: str
    menu: bool


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None:
        return default
    return value


def env_required(name: str, default: str) -> str:
    value = env(name, default)
    if value is None:
        raise RuntimeError(f"Variavel de ambiente obrigatoria ausente: {name}")
    return value


def normalize_start_time(raw_value: str) -> str:
    candidate = raw_value.strip()
    if not candidate:
        raise RuntimeError("SKY_START_TIME/--start-time nao pode ser vazio.")

    normalized = candidate.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise RuntimeError("SKY_START_TIME/--start-time deve estar em formato ISO-8601.") from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    else:
        parsed = parsed.astimezone(UTC)

    milliseconds = parsed.microsecond // 1000
    return parsed.strftime("%Y-%m-%dT%H:%M:%S") + f".{milliseconds:03d}Z"


def build_runtime_config(args: argparse.Namespace) -> RuntimeConfig:
    start_time_raw = str(args.start_time or env_required("SKY_START_TIME", DEFAULT_START_TIME))
    incident_criteria_json = str(
        args.incident_criteria_json or env("SKY_INCIDENT_CRITERIA_JSON", "")
    )
    page_size = args.page_size or int(env_required("SKY_PAGE_SIZE", str(DEFAULT_PAGE_SIZE)))
    max_pages = args.max_pages or int(env_required("SKY_MAX_PAGES", str(DEFAULT_MAX_PAGES)))
    auth_mode = str(args.auth_mode or env_required("SKY_AUTH_MODE", DEFAULT_AUTH_MODE))

    return RuntimeConfig(
        base_url=args.base_url,
        email=args.email or env("SKY_EMAIL"),
        password=args.password or env("SKY_PASSWORD"),
        tenant_id=args.tenant_id or env("SKY_TENANT_ID"),
        auth_path=args.auth_path,
        incidents_path=args.incidents_path,
        start_time=normalize_start_time(start_time_raw),
        incident_criteria_json=incident_criteria_json,
        page_size=page_size,
        max_pages=max_pages,
        pretty=args.pretty,
        auth_mode=auth_mode,
        menu=args.menu,
    )


def apply_runtime_config(args: argparse.Namespace) -> argparse.Namespace:
    config = build_runtime_config(args)
    args.base_url = config.base_url
    args.email = config.email
    args.password = config.password
    args.tenant_id = config.tenant_id
    args.auth_path = config.auth_path
    args.incidents_path = config.incidents_path
    args.start_time = config.start_time
    args.incident_criteria_json = config.incident_criteria_json
    args.page_size = config.page_size
    args.max_pages = config.max_pages
    args.pretty = config.pretty
    args.auth_mode = config.auth_mode
    args.menu = config.menu
    return args

from __future__ import annotations

import base64
import json
import os
from datetime import UTC, datetime, timedelta
from typing import cast
from urllib import error, parse, request

from skymonitor.types import (
    ConnectionResolution,
    IncidentCriteria,
    IncidentRecord,
    JSONValue,
)

DEFAULT_BASE_URLS = [
    "https://www.myshn.net",
    "https://www.myshn.eu",
    "https://www.myshn.ca",
    "https://www.govshn.net",
]


def _as_json_object(value: JSONValue) -> dict[str, JSONValue] | None:
    if isinstance(value, dict):
        return value
    return None


def _as_incident_record(value: JSONValue) -> IncidentRecord | None:
    if isinstance(value, dict):
        return cast(IncidentRecord, value)
    return None


def load_dotenv(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def _http_json(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    payload: dict[str, JSONValue] | None = None,
    timeout: int = 30,
) -> JSONValue:
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)

    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"

    req = request.Request(url=url, data=body, headers=req_headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
            if not content:
                return {}
            return cast(JSONValue, json.loads(content))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code} em {url}: {details}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Falha de rede em {url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Resposta nao-JSON em {url}") from exc


def _basic_auth_header(email: str, password: str) -> str:
    token = base64.b64encode(f"{email}:{password}".encode("utf-8")).decode("utf-8")
    return f"Basic {token}"


def _extract_token(payload: JSONValue) -> str:
    token_payload = _as_json_object(payload)
    if token_payload is None:
        raise RuntimeError("Resposta de token invalida (esperado objeto JSON).")

    payload_data = _as_json_object(token_payload.get("data")) or {}
    candidates = [
        token_payload.get("access_token"),
        token_payload.get("token"),
        token_payload.get("jwt"),
        payload_data.get("access_token"),
        payload_data.get("token"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate:
            return candidate
    raise RuntimeError("Token nao encontrado na resposta de autenticacao.")


def authenticate_legacy(base_url: str, auth_path: str, email: str, password: str) -> str:
    url = f"{base_url.rstrip('/')}/{auth_path.lstrip('/')}"
    response = _http_json("POST", url, payload={"email": email, "password": password})
    return _extract_token(response)


def authenticate_skyhigh(base_url: str, email: str, password: str) -> str:
    url = f"{base_url.rstrip('/')}/shnapi/rest/external/api/v1/token?grant_type=client_credentials"
    headers = {"Authorization": _basic_auth_header(email, password)}
    response = _http_json("POST", url, headers=headers)
    return _extract_token(response)


def authenticate_iam_tenant(base_url: str, email: str, password: str, tenant_id: str) -> str:
    step1_url = (
        f"{base_url.rstrip('/')}/shnapi/rest/external/api/v1/token"
        "?grant_type=password&token_type=iam"
    )
    step1_headers = {
        "Authorization": _basic_auth_header(email, password),
        "bps-tenant-id": tenant_id,
    }
    step1_response = _http_json("POST", step1_url, headers=step1_headers)
    iam_token = _extract_token(step1_response)

    step2_url = (
        f"{base_url.rstrip('/')}/neo/neo-auth-service/oauth/token"
        "?grant_type=iam_token&skip_audit=true"
    )
    step2_headers = {
        "x-iam-token": iam_token,
        "Content-Type": "application/json",
    }
    step2_response = _http_json("POST", step2_url, headers=step2_headers, payload={})
    return _extract_token(step2_response)


def _extract_incident_items(response: JSONValue) -> list[IncidentRecord]:
    if isinstance(response, list):
        return [item for raw in response if (item := _as_incident_record(raw)) is not None]

    response_data = _as_json_object(response)
    if response_data is None:
        return []

    for key in ("incidents", "items", "results", "data"):
        value = response_data.get(key)
        if isinstance(value, list):
            return [item for raw in value if (item := _as_incident_record(raw)) is not None]

    nested_body = _as_json_object(response_data.get("body"))
    if nested_body is not None:
        nested_incidents = nested_body.get("incidents")
        if isinstance(nested_incidents, list):
            return [
                item
                for raw in nested_incidents
                if (item := _as_incident_record(raw)) is not None
            ]

    if all(k in response_data for k in ("id", "severity")):
        record = _as_incident_record(response_data)
        return [record] if record is not None else []

    return []


def query_incidents_page(
    base_url: str,
    incidents_path: str,
    page_size: int,
    start_time: str | None,
    incident_criteria: IncidentCriteria | dict[str, JSONValue] | None,
    token: str | None,
    email: str,
    password: str,
) -> JSONValue:
    url = f"{base_url.rstrip('/')}/{incidents_path.lstrip('/')}"
    url = f"{url}?{parse.urlencode({'limit': page_size})}"
    payload: dict[str, JSONValue] = {}
    if start_time:
        payload["startTime"] = start_time
    if incident_criteria:
        payload["incidentCriteria"] = cast(JSONValue, incident_criteria)

    headers: dict[str, str] = {}
    if token:
        headers["x-access-token"] = token
        headers["Authorization"] = f"Bearer {token}"
    else:
        headers["Authorization"] = _basic_auth_header(email, password)

    return _http_json("POST", url, headers=headers, payload=payload)


def _extract_next_start_time(response: JSONValue) -> str | None:
    response_data = _as_json_object(response)
    if response_data is None:
        return None

    response_info = _as_json_object(response_data.get("responseInfo"))
    if response_info is not None:
        value = response_info.get("nextStartTime")
        if isinstance(value, str) and value:
            return value

    nested_body = _as_json_object(response_data.get("body"))
    if nested_body is not None:
        nested_info = _as_json_object(nested_body.get("responseInfo"))
        if nested_info is not None:
            value = nested_info.get("nextStartTime")
            if isinstance(value, str) and value:
                return value

    return None


def fetch_all_incidents(
    base_url: str,
    incidents_path: str,
    page_size: int,
    max_pages: int,
    start_time: str | None,
    incident_criteria: IncidentCriteria | dict[str, JSONValue] | None,
    token: str | None,
    email: str,
    password: str,
) -> list[IncidentRecord]:
    incidents: list[IncidentRecord] = []
    current_start_time = start_time

    for _ in range(max_pages):
        response = query_incidents_page(
            base_url=base_url,
            incidents_path=incidents_path,
            page_size=page_size,
            start_time=current_start_time,
            incident_criteria=incident_criteria,
            token=token,
            email=email,
            password=password,
        )
        page_items = _extract_incident_items(response)
        incidents.extend(page_items)
        next_start_time = _extract_next_start_time(response)

        if len(page_items) < page_size:
            break

        if not next_start_time or next_start_time == current_start_time:
            break

        current_start_time = next_start_time

    return incidents


def parse_base_candidates(args_base_url: str | None) -> list[str]:
    if args_base_url:
        return [args_base_url.strip()]

    from_env = os.getenv("SKY_BASE_URLS", "").strip()
    if from_env:
        return [b.strip() for b in from_env.split(",") if b.strip()]

    preferred = os.getenv("SKY_BASE_URL", "").strip()
    if preferred:
        return [preferred] + [b for b in DEFAULT_BASE_URLS if b != preferred]

    return DEFAULT_BASE_URLS[:]


def _require_arg(value: str | None, name: str) -> str:
    if value:
        return value
    raise RuntimeError(f"Parametro obrigatorio ausente: {name}")


def _dedupe(values: list[str]) -> list[str]:
    seen = set()
    out: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def build_start_time_for_days(days: int, now: datetime | None = None) -> str:
    if days < 1:
        raise ValueError("A quantidade de dias deve ser maior ou igual a 1.")

    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    else:
        current = current.astimezone(UTC)
    start_of_today = current.replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = start_of_today - timedelta(days=days - 1)
    return start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def filter_new_exchange_online_incidents(
    incidents: list[IncidentRecord],
) -> list[IncidentRecord]:
    filtered: list[IncidentRecord] = []
    for item in incidents:
        services = item.get("serviceNames")
        if item.get("status") != "new":
            continue
        if not isinstance(services, list):
            continue
        if "Microsoft Exchange Online" not in services:
            continue
        filtered.append(item)
    return filtered


def _parse_incident_criteria(raw_json: str) -> dict[str, JSONValue] | None:
    if not raw_json:
        return None

    parsed = json.loads(raw_json)
    if not isinstance(parsed, dict):
        raise RuntimeError("--incident-criteria-json deve ser um objeto JSON.")
    return parsed


def _build_auth_paths(args: object) -> list[str]:
    return _dedupe(
        [
            getattr(args, "auth_path", "") or "",
            os.getenv("SKY_AUTH_PATH", ""),
            "/auth/login",
        ]
    )


def _build_incidents_paths(args: object) -> list[str]:
    return _dedupe(
        [
            getattr(args, "incidents_path", "") or "",
            os.getenv("SKY_INCIDENTS_PATH", ""),
            "/shnapi/rest/external/api/v1/queryIncidents",
            "/incidents",
        ]
    )


def try_resolve_connection(
    base_candidates: list[str],
    auth_paths: list[str],
    incidents_paths: list[str],
    email: str,
    password: str,
    auth_mode: str,
    page_size: int,
    start_time: str | None,
    incident_criteria: IncidentCriteria | dict[str, JSONValue] | None,
    tenant_id: str | None,
) -> ConnectionResolution:
    errors: list[str] = []
    strict_token_only_mode = auth_mode == "iam-tenant"

    for base_url in base_candidates:
        token: str | None = None

        if auth_mode in ("auto", "iam-tenant") and tenant_id:
            try:
                token = authenticate_iam_tenant(base_url, email, password, tenant_id)
            except Exception as exc:
                errors.append(f"[{base_url}] iam-tenant falhou: {exc}")

        if token is None and auth_mode in ("auto", "skyhigh"):
            try:
                token = authenticate_skyhigh(base_url, email, password)
            except Exception as exc:
                errors.append(f"[{base_url}] skyhigh token falhou: {exc}")

        if token is None and auth_mode in ("auto", "legacy"):
            for auth_path in auth_paths:
                try:
                    token = authenticate_legacy(base_url, auth_path, email, password)
                    break
                except Exception as exc:
                    errors.append(f"[{base_url}] legacy {auth_path} falhou: {exc}")

        if strict_token_only_mode and token is None:
            errors.append(
                f"[{base_url}] incidente nao testado: autenticacao iam-tenant nao gerou token."
            )
            continue

        for incidents_path in incidents_paths:
            try:
                response = query_incidents_page(
                    base_url=base_url,
                    incidents_path=incidents_path,
                    page_size=1,
                    start_time=start_time,
                    incident_criteria=incident_criteria,
                    token=token if auth_mode != "basic-only" else None,
                    email=email,
                    password=password,
                )
                _ = _extract_incident_items(response)
                return {"base_url": base_url, "token": token, "incidents_path": incidents_path}
            except Exception as exc:
                mode_label = "token/basic" if auth_mode != "basic-only" else "basic"
                errors.append(
                    f"[{base_url}] incidente {incidents_path} ({mode_label}) falhou: {exc}"
                )

    raise RuntimeError("Nenhuma combinacao base/auth funcionou.\n" + "\n".join(errors))

#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
from typing import Any, Dict, List, Optional
from urllib import parse
from urllib import error, request

DEFAULT_BASE_URLS = [
    "https://www.myshn.net",
    "https://www.myshn.eu",
    "https://www.myshn.ca",
    "https://www.govshn.net",
]


def load_dotenv(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
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
    headers: Optional[Dict[str, str]] = None,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Any:
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
            return json.loads(content)
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


def _extract_token(payload: Any) -> str:
    if not isinstance(payload, dict):
        raise RuntimeError("Resposta de token invalida (esperado objeto JSON).")

    candidates = [
        payload.get("access_token"),
        payload.get("token"),
        payload.get("jwt"),
        (payload.get("data") or {}).get("access_token")
        if isinstance(payload.get("data"), dict)
        else None,
        (payload.get("data") or {}).get("token")
        if isinstance(payload.get("data"), dict)
        else None,
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
    # Step 1: IAM token using tenant header + basic auth
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

    # Step 2: Exchange IAM token for access token with tenant context
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


def _extract_incident_items(response: Any) -> List[Dict[str, Any]]:
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    if not isinstance(response, dict):
        return []

    for key in ("incidents", "items", "results", "data"):
        value = response.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    nested_body = response.get("body")
    if isinstance(nested_body, dict):
        nested_incidents = nested_body.get("incidents")
        if isinstance(nested_incidents, list):
            return [item for item in nested_incidents if isinstance(item, dict)]

    if all(k in response for k in ("id", "severity")):
        return [response]

    return []


def query_incidents_page(
    base_url: str,
    incidents_path: str,
    page_size: int,
    start_time: Optional[str],
    incident_criteria: Optional[Dict[str, Any]],
    token: Optional[str],
    email: str,
    password: str,
) -> Any:
    url = f"{base_url.rstrip('/')}/{incidents_path.lstrip('/')}"
    url = f"{url}?{parse.urlencode({'limit': page_size})}"
    payload: Dict[str, Any] = {}
    if start_time:
        payload["startTime"] = start_time
    if incident_criteria:
        payload["incidentCriteria"] = incident_criteria

    headers: Dict[str, str] = {}
    if token:
        headers["x-access-token"] = token
        headers["Authorization"] = f"Bearer {token}"
    else:
        headers["Authorization"] = _basic_auth_header(email, password)

    return _http_json("POST", url, headers=headers, payload=payload)


def _extract_next_start_time(response: Any) -> Optional[str]:
    if not isinstance(response, dict):
        return None

    response_info = response.get("responseInfo")
    if isinstance(response_info, dict):
        value = response_info.get("nextStartTime")
        if isinstance(value, str) and value:
            return value

    nested_body = response.get("body")
    if isinstance(nested_body, dict):
        nested_info = nested_body.get("responseInfo")
        if isinstance(nested_info, dict):
            value = nested_info.get("nextStartTime")
            if isinstance(value, str) and value:
                return value

    return None


def fetch_all_incidents(
    base_url: str,
    incidents_path: str,
    page_size: int,
    max_pages: int,
    start_time: Optional[str],
    incident_criteria: Optional[Dict[str, Any]],
    token: Optional[str],
    email: str,
    password: str,
) -> List[Dict[str, Any]]:
    incidents: List[Dict[str, Any]] = []
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


def parse_base_candidates(args_base_url: Optional[str]) -> List[str]:
    if args_base_url:
        return [args_base_url.strip()]

    from_env = os.getenv("SKY_BASE_URLS", "").strip()
    if from_env:
        return [b.strip() for b in from_env.split(",") if b.strip()]

    preferred = os.getenv("SKY_BASE_URL", "").strip()
    if preferred:
        return [preferred] + [b for b in DEFAULT_BASE_URLS if b != preferred]

    return DEFAULT_BASE_URLS[:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Busca incidentes da Skyhigh com autenticacao por e-mail/senha."
    )
    parser.add_argument("--base-url", default=None, help="Base URL da API")
    parser.add_argument("--email", default=os.getenv("SKY_EMAIL"), help="E-mail de autenticacao")
    parser.add_argument("--password", default=os.getenv("SKY_PASSWORD"), help="Senha de autenticacao")
    parser.add_argument(
        "--tenant-id",
        default=os.getenv("SKY_TENANT_ID"),
        help="Tenant ID para fluxo IAM multi-tenant (header bps-tenant-id)",
    )
    parser.add_argument(
        "--auth-path",
        default=None,
        help="Caminho do login legado (fallback)",
    )
    parser.add_argument(
        "--incidents-path",
        default=None,
        help="Caminho do endpoint de incidentes",
    )
    parser.add_argument(
        "--start-time",
        default=os.getenv("SKY_START_TIME", "2020-04-12T09:30:00.000"),
        help="Start time usado em queryIncidents (ex: 2020-04-12T09:30:00.000)",
    )
    parser.add_argument(
        "--incident-criteria-json",
        default=os.getenv("SKY_INCIDENT_CRITERIA_JSON", ""),
        help="JSON do campo incidentCriteria",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=int(os.getenv("SKY_PAGE_SIZE", "200")),
        help="Quantidade de itens por pagina",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=int(os.getenv("SKY_MAX_PAGES", "1000")),
        help="Limite de paginas para evitar loop infinito",
    )
    parser.add_argument("--pretty", action="store_true", help="Imprime JSON formatado")
    parser.add_argument(
        "--auth-mode",
        choices=["auto", "skyhigh", "legacy", "basic-only", "iam-tenant"],
        default=os.getenv("SKY_AUTH_MODE", "basic-only"),
        help="Modo de autenticacao",
    )
    return parser.parse_args()


def _require_arg(value: Optional[str], name: str) -> str:
    if value:
        return value
    raise RuntimeError(f"Parametro obrigatorio ausente: {name}")


def _dedupe(values: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def try_resolve_connection(
    base_candidates: List[str],
    auth_paths: List[str],
    incidents_paths: List[str],
    email: str,
    password: str,
    auth_mode: str,
    page_size: int,
    start_time: Optional[str],
    incident_criteria: Optional[Dict[str, Any]],
    tenant_id: Optional[str],
) -> Dict[str, Any]:
    errors: List[str] = []

    for base_url in base_candidates:
        token: Optional[str] = None

        # 0) fluxo IAM por tenant (quando usuario tem acesso a mais de um tenant)
        if auth_mode in ("auto", "iam-tenant") and tenant_id:
            try:
                token = authenticate_iam_tenant(base_url, email, password, tenant_id)
            except Exception as exc:
                errors.append(f"[{base_url}] iam-tenant falhou: {exc}")

        # 1) tenta token oficial Skyhigh
        if token is None and auth_mode in ("auto", "skyhigh"):
            try:
                token = authenticate_skyhigh(base_url, email, password)
            except Exception as exc:
                errors.append(f"[{base_url}] skyhigh token falhou: {exc}")

        # 2) fallback login legado (testa caminhos candidatos)
        if token is None and auth_mode in ("auto", "legacy"):
            for auth_path in auth_paths:
                try:
                    token = authenticate_legacy(base_url, auth_path, email, password)
                    break
                except Exception as exc:
                    errors.append(f"[{base_url}] legacy {auth_path} falhou: {exc}")

        # 3) valida endpoint de incidente com token ou basic (testa caminhos candidatos)
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


def main() -> int:
    load_dotenv()
    args = parse_args()

    try:
        email = _require_arg(args.email, "--email ou SKY_EMAIL")
        password = _require_arg(args.password, "--password ou SKY_PASSWORD")
        if args.auth_mode == "iam-tenant" and not args.tenant_id:
            raise RuntimeError("Informe --tenant-id ou SKY_TENANT_ID para auth-mode iam-tenant.")
        bases = parse_base_candidates(args.base_url)
        incident_criteria: Optional[Dict[str, Any]] = None
        if args.incident_criteria_json:
            parsed = json.loads(args.incident_criteria_json)
            if not isinstance(parsed, dict):
                raise RuntimeError("--incident-criteria-json deve ser um objeto JSON.")
            incident_criteria = parsed
        auth_paths = _dedupe(
            [
                args.auth_path or "",
                os.getenv("SKY_AUTH_PATH", ""),
                "/auth/login",
            ]
        )
        incidents_paths = _dedupe(
            [
                args.incidents_path or "",
                os.getenv("SKY_INCIDENTS_PATH", ""),
                "/shnapi/rest/external/api/v1/queryIncidents",
                "/incidents",
            ]
        )

        resolved = try_resolve_connection(
            base_candidates=bases,
            auth_paths=auth_paths,
            incidents_paths=incidents_paths,
            email=email,
            password=password,
            auth_mode=args.auth_mode,
            page_size=args.page_size,
            start_time=args.start_time,
            incident_criteria=incident_criteria,
            tenant_id=args.tenant_id,
        )

        incidents = fetch_all_incidents(
            base_url=resolved["base_url"],
            incidents_path=resolved["incidents_path"],
            page_size=args.page_size,
            max_pages=args.max_pages,
            start_time=args.start_time,
            incident_criteria=incident_criteria,
            token=resolved.get("token") if args.auth_mode != "basic-only" else None,
            email=email,
            password=password,
        )

        if args.pretty:
            print(json.dumps(incidents, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(incidents, ensure_ascii=False))

        print(f"Base escolhida: {resolved['base_url']}", file=sys.stderr)
        print(f"Endpoint de incidentes: {resolved['incidents_path']}", file=sys.stderr)
        print(f"Total de incidentes: {len(incidents)}", file=sys.stderr)
        return 0
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

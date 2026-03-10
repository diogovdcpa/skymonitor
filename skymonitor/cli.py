from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import cast

from skymonitor.api import (
    _build_auth_paths,
    _build_incidents_paths,
    _parse_incident_criteria,
    _require_arg,
    build_start_time_for_days,
    fetch_all_incidents,
    filter_exchange_online_incidents,
    filter_new_exchange_online_incidents,
    load_dotenv,
    parse_base_candidates,
    try_resolve_connection,
)
from skymonitor.config import apply_runtime_config
from skymonitor.types import (
    ConnectionResolution,
    IncidentRecord,
    InputFunc,
    JSONValue,
    MenuQueryExecutor,
    OutputFunc,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Busca incidentes da Skyhigh com autenticacao por e-mail/senha."
    )
    parser.add_argument("--base-url", default=None, help="Base URL da API")
    parser.add_argument("--email", default=None, help="E-mail de autenticacao")
    parser.add_argument("--password", default=None, help="Senha de autenticacao")
    parser.add_argument(
        "--tenant-id",
        default=None,
        help="Tenant ID para fluxo IAM multi-tenant (header bps-tenant-id)",
    )
    parser.add_argument("--auth-path", default=None, help="Caminho do login legado (fallback)")
    parser.add_argument(
        "--incidents-path",
        default=None,
        help="Caminho do endpoint de incidentes",
    )
    parser.add_argument(
        "--start-time",
        default=None,
        help="Start time usado em queryIncidents (ex: 2020-04-12T09:30:00.000)",
    )
    parser.add_argument(
        "--incident-criteria-json",
        default=None,
        help="JSON do campo incidentCriteria",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=None,
        help="Quantidade de itens por pagina",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Limite de paginas para evitar loop infinito",
    )
    parser.add_argument("--pretty", action="store_true", help="Imprime JSON formatado")
    parser.add_argument(
        "--auth-mode",
        choices=["auto", "skyhigh", "legacy", "basic-only", "iam-tenant"],
        default=None,
        help="Modo de autenticacao",
    )
    parser.add_argument(
        "--menu",
        action="store_true",
        help="Abre um menu interativo com consultas predefinidas.",
    )
    parser.add_argument(
        "--export-exchange-csv",
        action="store_true",
        help="Exporta em CSV os incidentes de Microsoft Exchange Online da janela fixa de 1 dia.",
    )
    parser.add_argument(
        "--export-dir",
        default=None,
        help="Diretorio de saida usado na exportacao CSV da janela fixa de 1 dia.",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Caminho do arquivo .env carregado antes da execucao.",
    )
    args = parser.parse_args(argv)
    return apply_runtime_config(args)


def execute_incident_query(
    args: argparse.Namespace,
    start_time: str,
    incident_criteria: dict[str, JSONValue] | None = None,
) -> list[IncidentRecord]:
    email = _require_arg(args.email, "--email ou SKY_EMAIL")
    password = _require_arg(args.password, "--password ou SKY_PASSWORD")
    if args.auth_mode == "iam-tenant" and not args.tenant_id:
        raise RuntimeError("Informe --tenant-id ou SKY_TENANT_ID para auth-mode iam-tenant.")

    resolved: ConnectionResolution = try_resolve_connection(
        base_candidates=parse_base_candidates(args.base_url),
        auth_paths=_build_auth_paths(args),
        incidents_paths=_build_incidents_paths(args),
        email=email,
        password=password,
        auth_mode=args.auth_mode,
        page_size=args.page_size,
        start_time=start_time,
        incident_criteria=incident_criteria,
        tenant_id=args.tenant_id,
    )

    incidents = fetch_all_incidents(
        base_url=resolved["base_url"],
        incidents_path=resolved["incidents_path"],
        page_size=args.page_size,
        max_pages=args.max_pages,
        start_time=start_time,
        incident_criteria=incident_criteria,
        token=resolved.get("token") if args.auth_mode != "basic-only" else None,
        email=email,
        password=password,
    )

    print(f"Base escolhida: {resolved['base_url']}", file=sys.stderr)
    print(f"Endpoint de incidentes: {resolved['incidents_path']}", file=sys.stderr)
    print(f"Total de incidentes: {len(incidents)}", file=sys.stderr)
    return incidents


def execute_menu_query(
    args: argparse.Namespace,
    mode: str,
    start_time: str,
) -> list[IncidentRecord]:
    incidents = execute_incident_query(args, start_time=start_time, incident_criteria=None)
    if mode == "exchange_new":
        return filter_new_exchange_online_incidents(incidents)
    if mode == "exchange":
        return filter_exchange_online_incidents(incidents)
    return incidents


def _prompt_days(
    input_func: InputFunc,
    output_func: OutputFunc,
) -> int:
    while True:
        raw = input_func("Quantidade de dias [1]: ").strip()
        if not raw:
            return 1
        try:
            return int(raw) if int(raw) >= 1 else -1
        except ValueError:
            output_func("Informe um numero inteiro maior ou igual a 1.")
            continue


def _format_incident_line(incident: IncidentRecord) -> str:
    info = incident.get("information")
    item_name = ""
    policy_name = ""
    if isinstance(info, dict):
        item_name = str(info.get("contentItemName", ""))
        policy_name = str(info.get("policyName", ""))

    incident_id = incident.get("incidentId", "")
    severity = incident.get("incidentRiskSeverity", "")
    status = incident.get("status", "")
    actor = incident.get("actorId", "")
    return (
        f"{incident_id} | severity={severity} | status={status} | "
        f"actor={actor} | arquivo={item_name} | policy={policy_name}"
    )


def _stringify_csv_value(value: JSONValue) -> str:
    if isinstance(value, list):
        parts = [str(item) for item in value if not isinstance(item, (dict, list))]
        return ";".join(parts)
    if isinstance(value, dict) or value is None:
        return ""
    return str(value)


def _extract_csv_field(incident: IncidentRecord, field_name: str) -> str:
    info = incident.get("information")

    if field_name == "from":
        actor_id = incident.get("actorId")
        if actor_id is not None:
            return str(actor_id)
        return ""

    if field_name == "to" and isinstance(info, dict):
        info_value = cast(dict[str, JSONValue], info).get("internalCollaborators")
        if info_value is not None:
            return _stringify_csv_value(info_value)
    return ""


def export_incidents_csv(
    incidents: list[IncidentRecord],
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["incident_id", "from", "to"])
        writer.writeheader()
        for incident in incidents:
            writer.writerow(
                {
                    "incident_id": incident.get("incidentId") or incident.get("id", ""),
                    "from": _extract_csv_field(incident, "from"),
                    "to": _extract_csv_field(incident, "to"),
                }
            )
    return output_path


def _render_banner(output_func: OutputFunc) -> None:
    output_func("========================================")
    output_func("            SkyhighMonitor")
    output_func("========================================")


def run_exchange_csv_export(
    args: argparse.Namespace,
    output_func: OutputFunc = print,
    execute_query: MenuQueryExecutor | None = None,
    now: datetime | None = None,
    export_dir: Path | None = None,
) -> int:
    current_time = now or datetime.now()
    csv_export_dir = export_dir or Path.cwd()
    query_executor = execute_query or (
        lambda mode, start_time: execute_menu_query(args, mode, start_time)
    )

    _render_banner(output_func)
    start_time = build_start_time_for_days(1, now=current_time)
    incidents = query_executor("exchange", start_time)
    output_path = csv_export_dir / current_time.strftime("exchange_incidents_%Y%m%d.csv")
    export_incidents_csv(incidents, output_path)

    output_func(f"Janela consultada desde: {start_time}")
    output_func(f"Total de incidentes exportados: {len(incidents)}")
    output_func(f"CSV exportado em: {output_path}")
    return 0


def run_interactive_menu(
    args: argparse.Namespace | None = None,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
    execute_query: MenuQueryExecutor | None = None,
    now: datetime | None = None,
    export_dir: Path | None = None,
) -> int:
    runtime_args = args or parse_args([])
    query_executor = execute_query or (
        lambda mode, start_time: execute_menu_query(runtime_args, mode, start_time)
    )
    csv_export_dir = export_dir or Path.cwd()

    _render_banner(output_func)

    while True:
        output_func("")
        output_func("1. Trazer todos os incidentes")
        output_func("2. Trazer incidentes new de Microsoft Exchange Online")
        output_func("3. Baixar CSV de incidentes de Microsoft Exchange Online (1 dia)")
        output_func("0. Sair")

        choice = input_func("Escolha uma opcao: ").strip()
        if choice == "0":
            output_func("Encerrando menu.")
            return 0

        if choice not in {"1", "2", "3"}:
            output_func("Opcao invalida. Escolha 1, 2, 3 ou 0.")
            continue

        if choice == "3":
            run_exchange_csv_export(
                args=runtime_args,
                output_func=output_func,
                execute_query=query_executor,
                now=now,
                export_dir=csv_export_dir,
            )
            continue

        days = _prompt_days(input_func, output_func)
        if days < 1:
            output_func("Informe um numero inteiro maior ou igual a 1.")
            continue

        start_time = build_start_time_for_days(days, now=now)
        mode = "all" if choice == "1" else "exchange_new"
        incidents = query_executor(mode, start_time)

        output_func(f"Janela consultada desde: {start_time}")
        output_func(f"Total de incidentes retornados: {len(incidents)}")
        for incident in incidents[:10]:
            output_func(_format_incident_line(incident))
        if len(incidents) > 10:
            output_func("Exibindo somente os 10 primeiros incidentes.")


def run_standard_cli(args: argparse.Namespace) -> int:
    incident_criteria = _parse_incident_criteria(args.incident_criteria_json)
    incidents = execute_incident_query(
        args,
        start_time=args.start_time,
        incident_criteria=incident_criteria,
    )

    if args.pretty:
        print(json.dumps(incidents, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(incidents, ensure_ascii=False))

    return 0


def main(argv: list[str] | None = None) -> int:
    cli_args = list(sys.argv[1:] if argv is None else argv)
    env_file = ".env"
    for index, token in enumerate(cli_args):
        if token == "--env-file" and index + 1 < len(cli_args):
            env_file = cli_args[index + 1]
            break
        if token.startswith("--env-file="):
            env_file = token.split("=", 1)[1]
            break

    load_dotenv(env_file)
    args = parse_args(cli_args)

    try:
        if getattr(args, "export_exchange_csv", False):
            export_dir = Path(args.export_dir) if args.export_dir else Path.cwd()
            return run_exchange_csv_export(args=args, export_dir=export_dir)
        if getattr(args, "menu", False) or not cli_args:
            return run_interactive_menu(args=args)
        return run_standard_cli(args)
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

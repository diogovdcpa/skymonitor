from __future__ import annotations

from collections.abc import Callable
from typing import NotRequired, TypeAlias, TypedDict

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONPrimitive | dict[str, "JSONValue"] | list["JSONValue"]


class TokenPayloadData(TypedDict, total=False):
    access_token: str
    token: str


class TokenPayload(TypedDict, total=False):
    access_token: str
    token: str
    jwt: str
    data: TokenPayloadData


class IncidentInformation(TypedDict, total=False):
    contentItemName: str
    policyName: str


class IncidentRecord(TypedDict, total=False):
    id: str
    incidentId: str
    severity: str
    incidentRiskSeverity: str
    status: str
    actorId: str
    instanceName: str
    serviceNames: list[str]
    information: IncidentInformation


class ResponseInfo(TypedDict, total=False):
    nextStartTime: str


class IncidentEnvelope(TypedDict, total=False):
    incidents: list[IncidentRecord]
    items: list[IncidentRecord]
    results: list[IncidentRecord]
    data: list[IncidentRecord]
    responseInfo: ResponseInfo
    body: NotRequired["IncidentEnvelope"]
    id: str
    severity: str


class ConnectionResolution(TypedDict):
    base_url: str
    incidents_path: str
    token: str | None


class IncidentCriteriaCategory(TypedDict, total=False):
    incidentType: str


class IncidentCriteria(TypedDict, total=False):
    categories: list[IncidentCriteriaCategory]


InputFunc: TypeAlias = Callable[[str], str]
OutputFunc: TypeAlias = Callable[[str], None]
MenuQueryExecutor: TypeAlias = Callable[[str, str], list[IncidentRecord]]

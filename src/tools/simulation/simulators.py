from typing import Any

from src.mcp_app import mcp
from src.simulators.rest_api_simulator import RestApiSimulator


_rest_api_simulator = RestApiSimulator()


@mcp.tool(
    name="simulate_http_api",
    version="1.0.0",
    title="Execute HTTP API Request",
    description=(
        "Execute an HTTP request against an API and return response metadata, "
        "the response body, and a parsed JSON payload when available."
    ),
    tags={"http", "api", "integration"},
    output_schema={
        "type": "object",
        "properties": {
            "ok": {"type": "boolean"},
            "status_code": {"type": ["integer", "null"]},
            "reason_phrase": {"type": ["string", "null"]},
            "headers": {"type": "object", "additionalProperties": {"type": "string"}},
            "body": {"type": ["string", "null"]},
            "json": {},
            "url": {"type": "string"},
            "cookies": {"type": "object", "additionalProperties": {"type": "string"}},
            "error": {"type": ["object", "null"]},
        },
        "required": ["ok", "status_code", "headers", "body", "json", "url"],
    },
    annotations={
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    meta={"category": "http-client", "safe_for_automatic_retry": False},
)
def simulate_http_api(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    body: Any = None,
    json_body: Any = None,
    form_data: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
    cookies: dict[str, str] | None = None,
    auth: list[str] | None = None,
    timeout: float | int = 30.0,
    follow_redirects: bool = True,
    verify: bool = True,
    content_type: str | None = None,
    accept: str | None = None,
    custom_kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute an HTTP request with common API integration options."""
    return _rest_api_simulator.execute(
        url=url,
        method=method,
        headers=headers,
        params=params,
        body=body,
        json_body=json_body,
        form_data=form_data,
        files=files,
        cookies=cookies,
        auth=auth,
        timeout=timeout,
        follow_redirects=follow_redirects,
        verify=verify,
        content_type=content_type,
        accept=accept,
        custom_kwargs=custom_kwargs,
    )


__all__ = ["simulate_http_api"]
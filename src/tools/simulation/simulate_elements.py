from typing import Any

from src.mcp_app import mcp
from src.service.simulator_service import execute_http_api


@mcp.tool(
    name="tool_execute_http_api",
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
def tool_execute_http_api(
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
    """Execute an HTTP request with common API integration options.

    Args:
        url: Fully qualified URL to call.
        method: HTTP method, such as GET, POST, PUT, PATCH, or DELETE.
        headers: Request headers keyed by header name.
        params: Query string parameters.
        body: Raw request body. Use either this or json_body, not both.
        json_body: JSON-compatible request payload. Use either this or body, not both.
        form_data: Form-encoded request fields.
        files: Multipart upload files accepted by httpx.
        cookies: Cookies keyed by cookie name.
        auth: Basic authentication as [username, password].
        timeout: Request timeout in seconds.
        follow_redirects: Whether redirects should be followed.
        verify: Whether TLS certificates should be verified.
        content_type: Optional Content-Type header value.
        accept: Optional Accept header value.
        custom_kwargs: Additional keyword arguments passed to httpx.request.

    Returns:
        Response metadata, response headers, response body, parsed JSON when
        available, and an error object when the HTTP request fails.
    """
    return execute_http_api(
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


__all__ = ["tool_execute_http_api"]

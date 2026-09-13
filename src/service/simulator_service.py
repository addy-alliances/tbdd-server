import json
from typing import Any

import httpx


def execute_http_api(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    body: Any = None,
    json_body: Any = None,
    form_data: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
    cookies: dict[str, str] | None = None,
    auth: tuple[str, str] | list[str] | None = None,
    timeout: float | int = 30.0,
    follow_redirects: bool = True,
    verify: bool = True,
    content_type: str | None = None,
    accept: str | None = None,
    custom_kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute an HTTP request using common API integration parameters.

    Args:
        url: Fully qualified URL to call.
        method: HTTP verb such as GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS.
        headers: Request headers dictionary.
        params: Query string parameters.
        body: Raw request body data. Use for text or binary payloads.
        json_body: JSON request payload.
        form_data: Form-encoded POST data.
        files: Multipart upload files payload.
        cookies: Cookie dictionary.
        auth: Basic auth tuple or list like ["username", "password"].
        timeout: Request timeout in seconds.
        follow_redirects: Whether to follow HTTP redirects.
        verify: Whether to verify TLS certificates.
        content_type: Overrides or sets the Content-Type header.
        accept: Sets the Accept header.
        custom_kwargs: Extra keyword arguments passed to httpx.request.

    Returns:
        A dictionary containing response metadata and payload.
    """
    request_method = (method or "GET").upper()
    normalized_headers = dict(headers or {})

    if accept is not None:
        normalized_headers["Accept"] = accept
    if content_type is not None and "Content-Type" not in normalized_headers:
        normalized_headers["Content-Type"] = content_type

    if json_body is not None and body is not None:
        raise ValueError("Use either 'body' or 'json_body', not both.")

    request_kwargs: dict[str, Any] = {
        "method": request_method,
        "url": url,
        "headers": normalized_headers,
        "params": params,
        "cookies": cookies,
        "timeout": timeout,
        "follow_redirects": follow_redirects,
        "verify": verify,
    }

    if auth is not None:
        request_kwargs["auth"] = tuple(auth) if isinstance(auth, list) else auth

    if json_body is not None:
        request_kwargs["json"] = json_body
    elif body is not None:
        if isinstance(body, (dict, list, int, float, bool)) and (
            "content-type" not in {k.lower(): v for k, v in normalized_headers.items()} or "json" in {k.lower(): v for k, v in normalized_headers.items()}.get("content-type", "").lower()
        ):
            request_kwargs["json"] = body
        else:
            request_kwargs["content"] = body if isinstance(body, (str, bytes)) else json.dumps(body)

    if form_data is not None:
        request_kwargs["data"] = form_data
    if files is not None:
        request_kwargs["files"] = files
    if custom_kwargs:
        request_kwargs.update(custom_kwargs)

    try:
        response = httpx.request(**request_kwargs)
    except httpx.HTTPError as exc:
        return {
            "ok": False,
            "error": {"type": exc.__class__.__name__, "message": str(exc)},
            "status_code": None,
            "headers": {},
            "body": None,
            "json": None,
            "url": url,
        }

    response_text = response.text
    response_json: Any = None
    if response_text:
        try:
            response_json = response.json()
        except ValueError:
            response_json = None

    return {
        "ok": response.is_success,
        "status_code": response.status_code,
        "reason_phrase": response.reason_phrase,
        "headers": dict(response.headers),
        "body": response_text,
        "json": response_json,
        "url": str(response.url),
        "cookies": dict(response.cookies),
    }


__all__ = ["execute_http_api"]

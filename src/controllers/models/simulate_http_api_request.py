from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SimulateHttpApiRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str
    method: str = "GET"
    headers: dict[str, str] | None = None
    params: dict[str, Any] | None = None
    body: Any = None
    json_body: Any = None
    form_data: dict[str, Any] | None = None
    files: dict[str, Any] | None = None
    cookies: dict[str, str] | None = None
    auth: list[str] | None = None
    timeout: float | int = Field(default=30.0, gt=0)
    follow_redirects: bool = True
    verify: bool = True
    content_type: str | None = None
    accept: str | None = None
    custom_kwargs: dict[str, Any] | None = None


__all__ = ["SimulateHttpApiRequest"]
from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base


class HttpApi(Base):
    __tablename__ = "http_api"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    method: Mapped[str] = mapped_column(String(16), nullable=False, default="GET")
    headers: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    params: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    body: Mapped[Any | None] = mapped_column(JSON, nullable=True)
    json_body: Mapped[Any | None] = mapped_column(JSON, nullable=True)
    form_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    files: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    cookies: Mapped[dict[str, str] | None] = mapped_column(JSON, nullable=True)
    auth: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    timeout: Mapped[float] = mapped_column(Float, nullable=False, default=30.0)
    follow_redirects: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    verify: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    accept: Mapped[str | None] = mapped_column(String(255), nullable=True)
    custom_kwargs: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    executions: Mapped[list["HttpApiExecution"]] = relationship(
        back_populates="http_api", cascade="all, delete-orphan"
    )
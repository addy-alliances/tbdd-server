from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base


class HttpApiExecution(Base):
    __tablename__ = "http_api_executions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    http_api_id: Mapped[str] = mapped_column(
        ForeignKey("http_api.id", ondelete="CASCADE"), nullable=False, index=True
    )
    request_headers: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    request_params: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    request_body: Mapped[Any | None] = mapped_column(JSON, nullable=True)
    response_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_headers: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    response_body: Mapped[Any | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    http_api: Mapped["HttpApi"] = relationship(back_populates="executions")
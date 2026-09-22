"""Create HTTP API and execution tables from PostgreSQL SQL files.

Revision ID: 0001_initial
Revises:
"""

from pathlib import Path

from alembic import op


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql_directory = Path(__file__).resolve().parents[1] / "sql"
    for filename in ("0001_http_api_up.sql", "0001_http_api_executions_up.sql"):
        op.execute((sql_directory / filename).read_text(encoding="utf-8"))


def downgrade() -> None:
    raise RuntimeError(
        "Downgrading 0001_initial is disabled because it would delete application data."
    )
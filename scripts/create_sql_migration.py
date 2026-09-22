import re
import secrets
import sys
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


ROOT = Path(__file__).resolve().parents[1]
SQL_DIRECTORY = ROOT / "alembic" / "sql"
VERSIONS_DIRECTORY = ROOT / "alembic" / "versions"


def slugify(message: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", message.lower()).strip("_")
    if not slug:
        raise ValueError("Migration message must contain at least one letter or number")
    return slug


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise SystemExit('Usage: make db-migration message="add description"')

    message = sys.argv[1].strip()
    revision = secrets.token_hex(6)
    slug = slugify(message)
    down_revision = ScriptDirectory.from_config(
        Config(str(ROOT / "alembic.ini"))
    ).get_current_head()
    stem = f"{revision}_{slug}"

    (SQL_DIRECTORY / f"{stem}_up.sql").write_text(
        "-- Add PostgreSQL upgrade SQL here.\n", encoding="utf-8"
    )
    (SQL_DIRECTORY / f"{stem}_down.sql").write_text(
        "-- Add rollback SQL here only when it is data-safe.\n", encoding="utf-8"
    )
    (VERSIONS_DIRECTORY / f"{stem}.py").write_text(
        f'''"""{message}."""\n\nfrom pathlib import Path\n\nfrom alembic import op\n\n\nrevision = "{revision}"\ndown_revision = {down_revision!r}\nbranch_labels = None\ndepends_on = None\n\n\ndef _sql_file(name: str) -> str:\n    return (Path(__file__).resolve().parents[1] / "sql" / name).read_text(encoding="utf-8")\n\n\ndef upgrade() -> None:\n    op.execute(_sql_file("{stem}_up.sql"))\n\n\ndef downgrade() -> None:\n    op.execute(_sql_file("{stem}_down.sql"))\n''',
        encoding="utf-8",
    )
    print(f"Created {stem}.py and matching SQL files")


if __name__ == "__main__":
    main()
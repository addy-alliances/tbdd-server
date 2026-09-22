# tbdd-server
test &amp; behavior driven development mcp server

## Storage and migrations

The application supports two storage backends:

```env
STORAGE_BACKEND=database
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/tbdd
```

Use file storage for local, single-instance development:

```env
STORAGE_BACKEND=file
FILE_STORAGE_PATH=data
```

Database migrations are PostgreSQL SQL files under `alembic/sql/` and are executed through Alembic. Run them manually with:

```text
alembic upgrade head
```

The Docker image runs `alembic upgrade head` before starting the application when `STORAGE_BACKEND` is `database` or unset. Run migrations as a single deployment step when using multiple application replicas.

Running the application again does not drop or recreate tables. Alembic records applied revisions in `alembic_version` and applies only pending revisions. For every schema change, add a new revision containing `ALTER TABLE` SQL; do not edit an already-applied migration. Downgrades are currently disabled because the initial downgrade would delete application data.

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database import Base
from src.database.models import HttpApi
from src.mcp_app import app
from src.storage.config import StorageSettings
from src.storage.database_repository import DatabaseRepository
from src.storage.enums import StorageBackend
from src.storage.factory import create_repository
from src.storage.file_repository import FileRepository
from src.controllers.storage_apis import get_storage_repository


def make_http_api(identifier: str = "api-1", url: str = "https://example.com") -> HttpApi:
    return HttpApi(
        id=identifier,
        url=url,
        method="GET",
        timeout=30.0,
        follow_redirects=True,
        verify=True,
    )


class StorageIntegrationTests(unittest.TestCase):
    def test_file_repository_save_and_list(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = FileRepository(HttpApi, Path(directory))
            repository.save(make_http_api())

            records = repository.list()

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].url, "https://example.com")
            self.assertEqual(json.loads(repository.path.read_text()), [{
                "id": "api-1",
                "url": "https://example.com",
                "method": "GET",
                "timeout": 30.0,
                "follow_redirects": True,
                "verify": True,
                "headers": None,
                "params": None,
                "body": None,
                "json_body": None,
                "form_data": None,
                "files": None,
                "cookies": None,
                "auth": None,
                "content_type": None,
                "accept": None,
                "custom_kwargs": None,
                "created_at": None,
                "updated_at": None,
            }])

    def test_database_repository_save_and_list(self) -> None:
        engine = create_engine("sqlite://")
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            repository = DatabaseRepository(HttpApi, session)
            repository.save(make_http_api())

            records = repository.list()

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].url, "https://example.com")

    def test_factory_selects_file_and_database_backends(self) -> None:
        settings = StorageSettings(StorageBackend.FILE, Path("data"))
        self.assertIsInstance(create_repository(HttpApi, settings), FileRepository)

        engine = create_engine("sqlite://")
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            settings = StorageSettings(StorageBackend.DATABASE, Path("data"))
            self.assertIsInstance(create_repository(HttpApi, settings, session), DatabaseRepository)

    def test_storage_api_lists_database_records(self) -> None:
        engine = create_engine("sqlite://")
        Base.metadata.create_all(engine)
        session = Session(engine)
        repository = DatabaseRepository(HttpApi, session)
        repository.save(make_http_api())

        app.dependency_overrides[get_storage_repository] = lambda: repository
        try:
            response = TestClient(app).get("/api/v1/storage/http-apis")
        finally:
            app.dependency_overrides.clear()
            session.close()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["url"], "https://example.com")

    def test_initial_migration_executes_sql_files(self) -> None:
        import importlib

        migration = importlib.import_module("alembic.versions.0001_initial")
        executed_sql: list[str] = []
        with patch.object(migration.op, "execute", side_effect=executed_sql.append):
            migration.upgrade()

        self.assertEqual(len(executed_sql), 2)
        self.assertIn("CREATE TABLE", executed_sql[0])
        self.assertIn("CREATE TABLE", executed_sql[1])


if __name__ == "__main__":
    unittest.main()
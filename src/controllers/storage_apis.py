from collections.abc import Generator
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.models import HttpApi
from src.service.storage_service import StorageService
from src.storage.config import StorageSettings
from src.storage.factory import create_repository
from src.storage.repository import StorageRepository


storage_router = APIRouter(prefix="/api/v1/storage", tags=["storage"])

def get_storage_repository(
    settings: StorageSettings = Depends(StorageSettings.from_environment),
) -> Generator[StorageRepository[HttpApi], None, None]:
    if settings.backend.value == "file":
        yield create_repository(HttpApi, settings)
        return

    database_generator = get_db()
    database = next(database_generator)
    try:
        yield create_repository(HttpApi, settings, database)
    finally:
        database_generator.close()

    repository: StorageRepository[HttpApi] = Depends(get_storage_repository),
) -> StorageService:
    return StorageService(repository)

def list_http_apis(service: StorageService = Depends(get_storage_service)) -> list[dict[str, Any]]:
    return [jsonable_encoder(http_api) for http_api in service.list_http_apis()]

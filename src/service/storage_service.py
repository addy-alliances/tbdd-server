from uuid import uuid4

from src.database.models import HttpApi
from src.storage.repository import StorageRepository


class StorageService:
    """Application service for storing and retrieving HTTP API definitions."""

    def __init__(self, repository: StorageRepository[HttpApi]):
        self.repository = repository

    def list_http_apis(self) -> list[HttpApi]:
        return self.repository.list()

    def save_http_api(self, http_api: HttpApi) -> HttpApi:
        if not http_api.id:
            http_api.id = str(uuid4())
        return self.repository.save(http_api)
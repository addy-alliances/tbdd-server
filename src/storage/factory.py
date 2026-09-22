from pathlib import Path
from typing import TypeVar

from sqlalchemy.orm import Session

from .config import StorageSettings
from .database_repository import DatabaseRepository
from .enums import StorageBackend
from .file_repository import FileRepository
from .repository import StorageRepository

ModelType = TypeVar("ModelType")

def create_repository(
    model_type: type[ModelType],
    settings: StorageSettings,
    session: Session | None = None,
) -> StorageRepository[ModelType]:
    if settings.backend == StorageBackend.FILE:
        return FileRepository(model_type, Path(settings.file_storage_path))

    if session is None:
        raise ValueError("A SQLAlchemy session is required for database storage")
    return DatabaseRepository(model_type, session)
from typing import Protocol, TypeVar

ModelType = TypeVar("ModelType")

class StorageRepository(Protocol[ModelType]):
    """Common persistence contract for file and database storage."""

    def list(self) -> list[ModelType]:
        """Return all stored models."""

    def save(self, model: ModelType) -> ModelType:
        """Create or replace a stored model."""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from .enums import StorageBackend

load_dotenv()


@dataclass(frozen=True)
class StorageSettings:
    backend: StorageBackend
    file_storage_path: Path

    @classmethod
    def from_environment(cls) -> "StorageSettings":
        backend_value = os.getenv("STORAGE_BACKEND", StorageBackend.DATABASE.value).lower()
        try:
            backend = StorageBackend(backend_value)
        except ValueError as error:
            valid_backends = ", ".join(item.value for item in StorageBackend)
            raise RuntimeError(
                f"STORAGE_BACKEND must be one of: {valid_backends}"
            ) from error

        return cls(
            backend=backend,
            file_storage_path=Path(os.getenv("FILE_STORAGE_PATH", "data")),
        )
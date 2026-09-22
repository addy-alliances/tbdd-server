from enum import Enum


class StorageBackend(str, Enum):
    DATABASE = "database"
    FILE = "file"
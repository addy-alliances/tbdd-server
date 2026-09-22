import json
import os
from datetime import date, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Generic, TypeVar

from sqlalchemy import inspect


ModelType = TypeVar("ModelType")


class FileRepository(Generic[ModelType]):
    """Persist SQLAlchemy model columns as records in a JSON file."""

    def __init__(self, model_type: type[ModelType], directory: Path):
        self.model_type = model_type
        self.path = directory / f"{model_type.__tablename__}.json"

    def list(self) -> list[ModelType]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as file:
            records = json.load(file)
        return [self._from_record(record) for record in records]

    def save(self, model: ModelType) -> ModelType:
        records = [self._to_record(item) for item in self.list()]
        record = self._to_record(model)
        identifier = record["id"]
        records = [item for item in records if item["id"] != identifier]
        records.append(record)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self.path.parent, delete=False
        ) as temporary_file:
            json.dump(records, temporary_file, indent=2)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, self.path)
        return model

    def _to_record(self, model: ModelType) -> dict[str, Any]:
        return {
            column.key: self._serialize(getattr(model, column.key))
            for column in inspect(self.model_type).columns
        }

    def _from_record(self, record: dict[str, Any]) -> ModelType:
        values = {
            column.key: self._deserialize(record.get(column.key), column.type.python_type)
            for column in inspect(self.model_type).columns
            if column.key in record
        }
        return self.model_type(**values)

    @staticmethod
    def _serialize(value: Any) -> Any:
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value

    @staticmethod
    def _deserialize(value: Any, value_type: type[Any]) -> Any:
        if value is None or value_type not in (datetime, date):
            return value
        return value_type.fromisoformat(value)


JsonFileRepository = FileRepository
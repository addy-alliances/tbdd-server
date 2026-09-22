from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session


class DatabaseRepository(Generic[ModelType]):

    def __init__(self, model_type: type[ModelType], session: Session):
        self.model_type = model_type
        self.session = session

    def list(self) -> list[ModelType]:
        return list(self.session.scalars(select(self.model_type)).all())

    def save(self, model: ModelType) -> ModelType:
        model = self.session.merge(model)
        self.session.commit()
        self.session.refresh(model)
        return model
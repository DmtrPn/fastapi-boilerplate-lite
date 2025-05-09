from abc import ABC, abstractmethod
import uuid
from app.infrastructure.models.example_model import ExampleModel
from app.domain.example_dto import ExampleCreateParams


class IExampleStorage(ABC):
    @abstractmethod
    def add(self, config: ExampleCreateParams) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: uuid.UUID) -> ExampleModel | None:
        raise NotImplementedError

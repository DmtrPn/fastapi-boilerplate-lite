import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod
from app.constants import ExampleStatus


@dataclass
class ExampleCreateParams:
    id: uuid.UUID
    status: ExampleStatus


@dataclass(frozen=True)
class ExampleDto:
    id: uuid.UUID
    status: ExampleStatus


class IExampleService(ABC):
    @abstractmethod
    async def create(self, params: ExampleCreateParams) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, example_id: uuid.UUID) -> ExampleDto | None:
        raise NotImplementedError

    @abstractmethod
    async def get_or_fail(self, example_id: uuid.UUID) -> ExampleDto:
        raise NotImplementedError

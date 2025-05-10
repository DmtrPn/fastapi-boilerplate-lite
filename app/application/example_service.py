import uuid

from app.application.abastract.i_example_storage import IExampleStorage
from app.domain.example_dto import IExampleService, ExampleCreateParams, ExampleDto
from app.infrastructure.example_storage import ExampleStorage, ExampleModel


class ExampleService(IExampleService):
    storage: IExampleStorage = ExampleStorage()

    async def get(self, example_id: uuid.UUID) -> ExampleDto | None:
        model = await self.storage.get(example_id)
        return self._to_dto(model) if model else None

    async def get_or_fail(self, example_id: uuid.UUID) -> ExampleDto:
        example = await self.storage.get(example_id)
        if example is None:
            raise ValueError(f"Example with id {example_id} not found")
        return self._to_dto(example)

    async def create(self, params: ExampleCreateParams) -> None:
        await self.storage.add(params)

    @staticmethod
    def _to_dto(model: ExampleModel) -> ExampleDto:
        return ExampleDto(id=model.id, status=model.status)

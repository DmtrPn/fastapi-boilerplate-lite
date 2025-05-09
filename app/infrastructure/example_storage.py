import uuid

from app.application.abastract.i_example_storage import IExampleStorage
from app.infrastructure.abstract.base_storage import BaseStorage
from app.infrastructure.models.example_model import ExampleModel
from app.domain.example_dto import ExampleCreateParams


class ExampleStorage(BaseStorage, IExampleStorage):
    def add(self, config: ExampleCreateParams):
        with self.session_scope() as session:
            owner = ExampleModel(id=config.id, status=config.status)
            session.add(owner)

    def get(self, id: uuid.UUID) -> ExampleModel | None:
        with self.session_scope(read_only=True) as session:
            return session.query(ExampleModel).filter_by(id=id).first()

from pydantic import BaseModel, Field
import uuid
from app.constants import ExampleStatus


class ExampleCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: ExampleStatus = ExampleStatus.active


class ExampleResponse(BaseModel):
    id: uuid.UUID
    status: ExampleStatus

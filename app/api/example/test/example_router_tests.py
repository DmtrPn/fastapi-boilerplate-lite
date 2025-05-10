import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.constants import ExampleStatus
from app.application.example_service import ExampleService
from app.domain.example_dto import ExampleCreateParams


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def example_service(storage_factory):
    service = ExampleService()
    service.storage = storage_factory(service.storage.__class__)
    return service


@pytest.fixture
def example_id():
    return uuid.uuid4()


async def test_create_example(client, example_service, example_id):
    test_data = {"id": str(example_id), "status": ExampleStatus.active.value}

    response = client.post("/example", json=test_data)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == str(example_id)
    assert data["status"] == ExampleStatus.active.value

    example = await example_service.get(example_id)
    assert example is not None
    assert example.id == example_id
    assert example.status == ExampleStatus.active


async def test_get_example(client, example_service, example_id):
    config = ExampleCreateParams(id=example_id, status=ExampleStatus.active)
    await example_service.create(config)

    response = client.get(f"/example/{example_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(example_id)
    assert data["status"] == ExampleStatus.active.value


def test_get_example_not_found(client, example_service, example_id):
    response = client.get(f"/example/{example_id}")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]

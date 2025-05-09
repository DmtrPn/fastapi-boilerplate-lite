from fastapi import APIRouter, HTTPException, Depends
import uuid
from app.api.example.models import ExampleCreate, ExampleResponse
from app.application.example_service import ExampleService
from app.domain.example_dto import ExampleCreateParams

router = APIRouter(prefix="/example", tags=["example"])


# Dependency to get the example service
def get_example_service():
    return ExampleService()


@router.post("", response_model=ExampleResponse, status_code=201)
def create_example(example: ExampleCreate, service: ExampleService = Depends(get_example_service)):
    # Convert Pydantic model to DTO
    params = ExampleCreateParams(id=example.id, status=example.status)

    # Create example
    service.create(params)

    # Return the created example
    return ExampleResponse(id=example.id, status=example.status)


@router.get("/{example_id}", response_model=ExampleResponse)
def get_example(example_id: uuid.UUID, service: ExampleService = Depends(get_example_service)):
    # Get example by ID
    example = service.get(example_id)

    # Raise 404 if example not found
    if example is None:
        raise HTTPException(status_code=404, detail=f"Example with ID {example_id} not found")

    # Return the example
    return ExampleResponse(id=example.id, status=example.status)

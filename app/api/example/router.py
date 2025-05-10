from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
import uuid

from app.api.example.models import ExampleCreate, ExampleResponse
from app.application.example_service import ExampleService
from app.domain.example_dto import ExampleCreateParams
from app.api.utils.serializer import serializer, COOKIE_NAME

example_router = APIRouter(prefix="/example", tags=["example"])


# Dependency to get the example service
def get_example_service():
    return ExampleService()


@example_router.post("", response_model=ExampleResponse, status_code=201)
async def create_example(example: ExampleCreate, service: ExampleService = Depends(get_example_service)):
    # Convert Pydantic model to DTO
    params = ExampleCreateParams(id=example.id, status=example.status)

    # Create example
    await service.create(params)

    # Return the created example
    return ExampleResponse(id=example.id, status=example.status)


@example_router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(example_id: uuid.UUID, service: ExampleService = Depends(get_example_service)):
    # Get example by ID
    example = await service.get(example_id)

    # Raise 404 if example not found
    if example is None:
        raise HTTPException(status_code=404, detail=f"Example with ID {example_id} not found")

    # Return the example
    return ExampleResponse(id=example.id, status=example.status)


@example_router.post("/cookie/set")
def set_encrypted_cookie(response: Response):
    data = {"username": "user123", "role": "admin"}
    encrypted_data = serializer.dumps(data)
    response.set_cookie(key=COOKIE_NAME, value=encrypted_data, httponly=True)
    return {"message": "Encrypted cookie set"}


@example_router.get("/cookie/get")
def get_encrypted_cookie(request: Request):
    encrypted_data = request.cookies.get(COOKIE_NAME)
    if not encrypted_data:
        return JSONResponse(status_code=400, content={"error": "No cookie found"})
    try:
        data = serializer.loads(encrypted_data)
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid or tampered cookie"})
    return {"decrypted_data": data}

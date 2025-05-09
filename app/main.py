from fastapi import FastAPI
from app.api.example.router import router as example_router

# Create FastAPI app
app = FastAPI(
    title="Example Service API",
    description="API for managing examples",
    version="1.0.0",
)

# Include routers
app.include_router(example_router)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Example Service API"}


# Run with: uvicorn app.api.main:app --reload

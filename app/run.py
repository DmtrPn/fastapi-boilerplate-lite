import uvicorn
from app.config import settings
import app.logger  # noqa

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        log_level="info",
        reload=False,
    )

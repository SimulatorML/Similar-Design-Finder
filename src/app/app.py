from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator

from src.config import settings
from src.routers.main import router as finder_router

app = FastAPI()
app.include_router(finder_router, prefix=settings.API_VERSION_STR, tags=["Documents"])

Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health() -> Response:
    return Response(status_code=status.HTTP_200_OK)

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator

from src.config import settings
from src.repositories import UserRepository
from src.routers.main import router as finder_router
from src.routers.schemas import RoleSchema
from src.services.user import UserService
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        role_data = RoleSchema(**settings.roles["user"])
        await UserService(UserRepository()).ensure_role_exists(role_data=role_data)
        logger.info("Roles ensured successfully.")

        yield

    except Exception as exp:
        logger.error(f"Failed during lifespan initialization: {exp}")
        raise exp


app = FastAPI(lifespan=lifespan)
app.include_router(finder_router, prefix=settings.API_VERSION_STR, tags=["Documents"])

Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health() -> Response:
    return Response(status_code=status.HTTP_200_OK)

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ENV = os.getenv("ENV", "local")

load_dotenv(Path(f".env.{ENV}"))


class Settings(BaseSettings):
    PG_USER: str = os.getenv("PG_USER")
    PG_PASS: str = os.getenv("PG_PASSWORD")
    PG_HOST: str = os.getenv("PG_HOST")
    PG_PORT: str = os.getenv("PG_PORT")
    PG_DB: str = os.getenv("PG_DB")

    database_uri: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    API_VERSION_STR: str = os.getenv("API_VERSION_STR", "/api/v1")

    COLLECTION_NAME: str = "design_docs"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"  # just for example
    MODEL_CACHE_DIR: Path = Path(".model_cache")


settings = Settings()

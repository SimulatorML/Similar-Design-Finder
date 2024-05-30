import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(Path(".env"))


class Settings(BaseSettings):
    PG_USER: str = os.getenv("PG_USER")
    PG_PASS: str = os.getenv("PG_PASSWORD")
    PG_HOST: str = os.getenv("PG_HOST")
    PG_PORT: str = os.getenv("PG_PORT")
    PG_DB: str = os.getenv("PG_DB")

    database_uri: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    API_VERSION_STR: str = os.getenv("API_VERSION_STR", "/api/v1")


settings = Settings()

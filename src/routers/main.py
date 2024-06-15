from typing import Annotated

from fastapi import APIRouter, Depends

from src.config import settings
from src.routers.schemas import FinderResult, FindRequest
from src.services.finder import FinderService

router = APIRouter()


async def get_finder() -> FinderService:
    return FinderService(
        collection_name=settings.COLLECTION_NAME,
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_cache_dir=settings.MODEL_CACHE_DIR,
    )


@router.post("/find", response_model=FinderResult)
async def find(payload: FindRequest, finder: Annotated[FinderService, Depends(get_finder)]) -> FinderResult:
    return await finder.find(payload)

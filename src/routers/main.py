from typing import Annotated

from fastapi import APIRouter, Depends

from src.config import settings
from src.routers.schemas import FinderResult, FindRequest
from src.services.finder import Finder

router = APIRouter()


async def get_finder() -> Finder:
    return await Finder.create(collection_name=settings.COLLECTION_NAME, model_name=settings.EMBEDDING_MODEL_NAME)


@router.post("/find", response_model=FinderResult)
async def find(payload: FindRequest, finder: Annotated[Finder, Depends(get_finder)]) -> FinderResult:
    return await finder.find(payload)

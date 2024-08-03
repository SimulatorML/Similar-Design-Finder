from typing import Annotated

from fastapi import APIRouter, Depends

from src.config import settings
from src.repositories import CollectionRepository, DocsRepository, UserRepository
from src.routers.schemas import FinderResult, FindRequest, UserCreateSchema
from src.services.finder import FinderService
from src.services.user import UserService

router = APIRouter()


async def get_user() -> UserService:
    user_repository = UserRepository()
    return UserService(user_repository=user_repository)


async def get_finder() -> FinderService:
    return FinderService(
        collection_name=settings.COLLECTION_NAME,
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_cache_dir=settings.MODEL_CACHE_DIR,
        collection_repository=CollectionRepository(),
        docs_repository=DocsRepository(),
    )


@router.post("/register")
async def register(payload: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user)]) -> None:
    return await user_service.register(payload)


@router.post("/find", response_model=FinderResult)
async def find(payload: FindRequest, finder: Annotated[FinderService, Depends(get_finder)]) -> FinderResult:
    return await finder.find(payload)


@router.post("/feedback")
async def feedback(payload: dict, finder: Annotated[FinderService, Depends(get_finder)]) -> None:
    return await finder.process_feedback(payload)

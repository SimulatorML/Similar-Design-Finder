from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.config import settings
from src.repositories import CollectionRepository, DocsRepository, UserActivityRepository, UserRepository
from src.routers.schemas import Feedback, FinderResult, FindRequest, UserCreateSchema
from src.services.finder import FinderService
from src.services.user import UserService

router = APIRouter()


@lru_cache
async def get_user() -> UserService:
    user_repository = UserRepository()
    return UserService(user_repository=user_repository)


@lru_cache
async def get_finder() -> FinderService:
    return FinderService(
        collection_name=settings.COLLECTION_NAME,
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_cache_dir=settings.MODEL_CACHE_DIR,
        collection_repository=CollectionRepository(),
        docs_repository=DocsRepository(),
        users_repository=UserRepository(),
        user_activity_repository=UserActivityRepository(),
    )


@router.post("/register")
async def register(payload: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user)]) -> None:
    return await user_service.register(payload)


@router.post("/find", response_model=FinderResult)
async def find(payload: FindRequest, finder: Annotated[FinderService, Depends(get_finder)]) -> FinderResult:
    return await finder.find(payload)


@router.post("/feedback")
async def feedback(payload: Feedback, finder: Annotated[FinderService, Depends(get_finder)]) -> None:
    success = await finder.process_feedback(payload)
    if success:
        return {"message": "Feedback submitted successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to submit feedback.")

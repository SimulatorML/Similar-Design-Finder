from typing import Annotated

from fastapi import APIRouter, Depends

from src.routers.schemas import FinderResult, FindRequest
from src.services.finder import Finder

router = APIRouter()


def get_finder() -> Finder:
    return Finder()


@router.post("/find", response_model=FinderResult)
def find(payload: FindRequest, finder: Annotated[Finder, Depends(get_finder)]) -> FinderResult:
    return finder.find(payload)

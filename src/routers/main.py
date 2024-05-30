from fastapi import APIRouter

from src.routers.schemas import FinderResult, Payload
from src.services.finder import Finder

router = APIRouter()

finder = Finder()


@router.post("/find", response_model=FinderResult)
def find(payload: Payload) -> FinderResult:
    return finder.find(payload)

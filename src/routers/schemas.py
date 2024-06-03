import uuid

from pydantic import BaseModel


class FindRequest(BaseModel):
    user_id: int | uuid.UUID
    query: str
    source: str


class DesignDocument(BaseModel):
    doc_id: uuid.UUID
    link: str
    score: float
    metadata: dict | None


class FinderResult(BaseModel):
    query: str
    response: str
    response_time: int
    documents: list[DesignDocument]

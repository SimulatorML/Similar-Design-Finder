import uuid

from pydantic import BaseModel


class FindRequest(BaseModel):
    user_id: int | uuid.UUID
    request: str
    source: str


class DocumentSchema(BaseModel):
    doc_id: uuid.UUID
    company: str | None
    industry: str | None
    title: str | None
    description: str | None
    summarization: str | None
    tags: str | None
    year: int | None
    source: str | None
    status: str | None
    s3_link: str
    score: float
    metadata: dict | None


class FinderResult(BaseModel):
    request: str
    documents: list[DocumentSchema]

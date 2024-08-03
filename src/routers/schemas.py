import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    telegram_id: int | None
    username: str | None
    email: EmailStr | None
    password: str | None


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
    query_id: uuid.UUID
    request: str
    documents: list[DocumentSchema]


class FeedbackLabel(str, Enum):
    like = "like"
    dislike = "dislike"


class Feedback(BaseModel):
    query_id: uuid.UUID
    label: FeedbackLabel


class RoleSchema(BaseModel):
    role_name: str
    permissions: dict

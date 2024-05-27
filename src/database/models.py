import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from src.database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, unique=True, nullable=False)
    permissions = Column(JSON, nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(Integer, unique=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    created_at = Column(DateTime(timezone=False), default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)


class Document(Base):
    __tablename__ = "documents"

    doc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    summarization = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    source = Column(String, nullable=True)
    status = Column(String, nullable=True)
    s3_link = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())


class Embedding(Base):
    __tablename__ = "embeddings"

    embedding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id"))
    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.collection_id"))
    text = Column(String, nullable=False)
    embedding = Column(Vector(1024), nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())


class Collection(Base):
    __tablename__ = "collections"

    collection_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())


class FinderQueries(Base):
    __tablename__ = "finder_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    response_time = Column(Integer, nullable=False)
    metadata = Column(JSON, nullable=True)
    feedback = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=False), default=func.now())


class QueriesClicks(Base):
    __tablename__ = "queries_clicks"

    click_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("finder_queries.query_id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    click_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())

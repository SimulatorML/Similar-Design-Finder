import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
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

    role = relationship("Role", back_populates="users")
    finder_queries = relationship("FinderQueries", back_populates="user", cascade="all, delete-orphan")
    queries_clicks = relationship("QueriesClicks", back_populates="user", cascade="all, delete-orphan")


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

    embeddings = relationship("Embedding", back_populates="document", cascade="all, delete-orphan")
    finder_queries = relationship("FinderQueryDocument", back_populates="document", cascade="all, delete-orphan")
    queries_clicks = relationship("QueriesClicks", back_populates="document", cascade="all, delete-orphan")


class Embedding(Base):
    __tablename__ = "embeddings"

    embedding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"))
    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.collection_id", ondelete="CASCADE"))
    text = Column(String, nullable=False)
    embedding = Column(Vector(1024), nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())

    document = relationship("Document", back_populates="embeddings")
    collection = relationship("Collection", back_populates="embeddings")


class Collection(Base):
    __tablename__ = "collections"

    collection_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())

    embeddings = relationship("Embedding", back_populates="collection", cascade="all, delete-orphan")


class FinderQueries(Base):
    __tablename__ = "finder_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    response_time = Column(Integer, nullable=False)
    metadata_info = Column(JSON, nullable=True)
    feedback = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=False), default=func.now())

    user = relationship("User", back_populates="finder_queries")
    documents = relationship("FinderQueryDocument", back_populates="finder_query", cascade="all, delete-orphan")
    queries_clicks = relationship("QueriesClicks", back_populates="finder_query", cascade="all, delete-orphan")


class QueriesClicks(Base):
    __tablename__ = "queries_clicks"

    click_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("finder_queries.query_id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=False), default=func.now())

    finder_query = relationship("FinderQueries", back_populates="queries_clicks")
    user = relationship("User", back_populates="queries_clicks")
    document = relationship("Document", back_populates="queries_clicks")


class FinderQueryDocument(Base):
    __tablename__ = "finder_query_documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("finder_queries.query_id", ondelete="CASCADE"), nullable=False)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"), nullable=False)

    finder_query = relationship("FinderQueries", back_populates="documents")
    document = relationship("Document", back_populates="finder_queries")

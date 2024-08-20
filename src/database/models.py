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

    user = relationship("User", back_populates="role")


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

    role = relationship("Role", back_populates="user")
    finder_query = relationship("FinderQuery", back_populates="user", cascade="all, delete-orphan")
    query_click = relationship("QueryClick", back_populates="user", cascade="all, delete-orphan")


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

    embedding = relationship("Embedding", back_populates="document", cascade="all, delete-orphan")
    finder_query = relationship("FinderQueryDocument", back_populates="document", cascade="all, delete-orphan")
    query_click = relationship("QueryClick", back_populates="document", cascade="all, delete-orphan")


class Embedding(Base):
    __tablename__ = "embeddings"

    embedding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"))
    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.collection_id", ondelete="CASCADE"))
    text = Column(String, nullable=False)
    embedding = Column(Vector, nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())

    document = relationship("Document", back_populates="embedding")
    collection = relationship("Collection", back_populates="embedding")


class Collection(Base):
    __tablename__ = "collections"

    collection_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    model = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), default=func.now())

    embedding = relationship("Embedding", back_populates="collection", cascade="all, delete-orphan")


class FinderQuery(Base):
    __tablename__ = "finder_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    response_time = Column(Integer, nullable=False)
    metadata_info = Column(JSON, nullable=True)
    feedback = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=False), default=func.now())

    user = relationship("User", back_populates="finder_query")
    document = relationship("FinderQueryDocument", back_populates="finder_query", cascade="all, delete-orphan")
    query_click = relationship("QueryClick", back_populates="finder_query", cascade="all, delete-orphan")


class QueryClick(Base):
    __tablename__ = "queries_clicks"

    click_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("finder_queries.query_id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=False), default=func.now())

    finder_query = relationship("FinderQuery", back_populates="query_click")
    user = relationship("User", back_populates="query_click")
    document = relationship("Document", back_populates="query_click")


class FinderQueryDocument(Base):
    __tablename__ = "finder_query_documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("finder_queries.query_id", ondelete="CASCADE"), nullable=False)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"), nullable=False)
    rank = Column(Integer)

    finder_query = relationship("FinderQuery", back_populates="document")
    document = relationship("Document", back_populates="finder_query")

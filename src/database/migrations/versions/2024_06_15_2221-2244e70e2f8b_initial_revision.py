"""Initial revision

Revision ID: 2244e70e2f8b
Revises:
Create Date: 2024-06-15 22:21:24.866948

"""

from collections.abc import Sequence

import pgvector
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2244e70e2f8b"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "collections",
        sa.Column("collection_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("collection_id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "documents",
        sa.Column("doc_id", sa.UUID(), nullable=False),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("industry", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("summarization", sa.String(), nullable=True),
        sa.Column("tags", sa.String(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("s3_link", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("doc_id"),
    )
    op.create_table(
        "roles",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("role_name", sa.String(), nullable=False),
        sa.Column("permissions", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("role_id"),
        sa.UniqueConstraint("role_name"),
    )
    op.create_table(
        "embeddings",
        sa.Column("embedding_id", sa.UUID(), nullable=False),
        sa.Column("doc_id", sa.UUID(), nullable=True),
        sa.Column("collection_id", sa.UUID(), nullable=True),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["collection_id"], ["collections.collection_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["doc_id"], ["documents.doc_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("embedding_id"),
    )
    op.create_table(
        "users",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.role_id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_table(
        "finder_queries",
        sa.Column("query_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("query", sa.String(), nullable=False),
        sa.Column("response", sa.String(), nullable=False),
        sa.Column("response_time", sa.Integer(), nullable=False),
        sa.Column("metadata_info", sa.JSON(), nullable=True),
        sa.Column("feedback", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("query_id"),
    )
    op.create_table(
        "finder_query_documents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("query_id", sa.UUID(), nullable=False),
        sa.Column("doc_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["doc_id"], ["documents.doc_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["query_id"], ["finder_queries.query_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "queries_clicks",
        sa.Column("click_id", sa.UUID(), nullable=False),
        sa.Column("query_id", sa.UUID(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("doc_id", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["doc_id"], ["documents.doc_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["query_id"], ["finder_queries.query_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("click_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("queries_clicks")
    op.drop_table("finder_query_documents")
    op.drop_table("finder_queries")
    op.drop_table("users")
    op.drop_table("embeddings")
    op.drop_table("roles")
    op.drop_table("documents")
    op.drop_table("collections")
    # ### end Alembic commands ###

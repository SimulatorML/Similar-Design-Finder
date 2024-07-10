import uuid

from sqlalchemy import select

from src.database import async_session_maker
from src.database.models import Document, Embedding
from src.routers.schemas import DocumentSchema


class DocsRepository:
    def __init__(self) -> None:
        pass

    async def add_document(self, doc_data: DocumentSchema, embedding_data: dict) -> bool:
        try:
            async with async_session_maker() as session:
                document = Document(
                    doc_id=doc_data.doc_id,
                    company=doc_data.company,
                    industry=doc_data.industry,
                    title=doc_data.title,
                    description=doc_data.description,
                    summarization=doc_data.summarization,
                    tags=doc_data.tags,
                    year=doc_data.year,
                    source=doc_data.source,
                    status=doc_data.status,
                    s3_link=doc_data.s3_link,
                )
                session.add(document)

                embedding = Embedding(
                    doc_id=embedding_data["doc_id"],
                    collection_id=embedding_data["collection_id"],
                    text=embedding_data["text"],
                    embedding=embedding_data["embedding"],
                )
                session.add(embedding)

                await session.commit()

                return True
        except Exception:
            return False

    async def get_similarities(
        self, request_embedding: list[float], collection_id: uuid.UUID, limit: int = 5
    ) -> tuple[list[uuid.UUID], dict]:
        async with async_session_maker() as session:
            query = (
                select(
                    Embedding.doc_id,
                    Embedding.embedding.cosine_distance(request_embedding).label("cosine_distance"),
                )
                .where(Embedding.collection_id == collection_id)
                .order_by("cosine_distance")
                .limit(limit)
            )

            result = await session.execute(query)
            rows = result.fetchall()
            doc_ids = [row[0] for row in rows]
            similarities = {row[0]: 1 - row[1] for row in rows}

            return doc_ids, similarities

    async def query_similar_docs(self, doc_ids: list[uuid.UUID], similarities: dict) -> list[DocumentSchema]:
        async with async_session_maker() as session:
            documents = await session.execute(select(Document).where(Document.doc_id.in_(doc_ids)))
            documents = documents.scalars().all()

            docs = [
                DocumentSchema(
                    doc_id=doc.doc_id,
                    company=doc.company,
                    industry=doc.industry,
                    title=doc.title,
                    description=doc.description,
                    summarization=doc.summarization,
                    tags=doc.tags,
                    year=doc.year,
                    source=doc.source,
                    status=doc.status,
                    s3_link=doc.s3_link,
                    score=similarities[doc.doc_id],
                    metadata=None,
                )
                for doc in documents
            ]

            return sorted(docs, key=lambda doc: doc.score, reverse=True)

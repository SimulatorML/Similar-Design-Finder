from sqlalchemy import select

from src.database import async_session_maker
from src.database.models import Collection, Document, Embedding
from src.routers.schemas import DocumentSchema


class Postgres:
    """
    A class for interacting with the Postgres Database

    Parameters
    ----------
    collection : Collection
        The collection instance to be managed by this class.

    Examples
    --------
    >>> import asyncio
    >>> postgres = asyncio.run(Postgres.create())
    >>> print(type(postgres))
    <class '__main__.Postgres'>
    """

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    @classmethod
    async def create(cls, collection_name: str, model_name: str) -> "Postgres":  # noqa: ANN102
        collection = await cls.get_or_create_collection(name=collection_name, model=model_name)
        return cls(collection)

    @staticmethod
    async def get_or_create_collection(name: str, model: str) -> Collection:
        async with async_session_maker() as session:
            collection = await session.execute(select(Collection).where(Collection.name == name))
            collection = collection.scalar()

            if not collection:
                collection = Collection(
                    name=name,
                    model=model,
                )
                session.add(collection)
                await session.commit()

            return collection

    async def add_document(self, doc_data: DocumentSchema, embedding_data: dict) -> Document:
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
                collection_id=self.collection.collection_id,
                text=embedding_data["text"],
                embedding=embedding_data["embedding"],
            )
            session.add(embedding)

            await session.commit()

    async def retrieve_docs(self, request_embedding: list[float]) -> list:  # list[DocumentSchema]:
        async with async_session_maker() as session:
            query = (
                select(
                    Embedding.doc_id,
                    (1 - Embedding.embedding.cosine_distance(request_embedding)).label("cosine_similarity"),
                )
                .order_by("cosine_similarity")
                .limit(5)
            )

            result = await session.execute(query)
            rows = result.fetchall()
            doc_ids = [row[0] for row in rows]
            similarities = {row[0]: row[1] for row in rows}

            documents = await session.execute(select(Document).where(Document.doc_id.in_(doc_ids)))
            documents = documents.scalars().all()

            return [
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

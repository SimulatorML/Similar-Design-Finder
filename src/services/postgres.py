from sqlalchemy import select

from src.database import async_session_maker
from src.database.models import Collection, Document, Embedding
from src.routers.schemas import DocumentSchema


class Postgres:
    async def get_or_create_collection(self, name: str, model: str) -> Collection:
        async with async_session_maker() as session:
            collection = await self.session.execute(select(Collection).where(Collection.name == name))
            collection = collection.scalar()

            if not collection:
                collection = Collection(
                    name=name,
                    model=model,
                )
                session.add(collection)
                await session.commit()

            return collection

    async def add_document(self, doc_data: DocumentSchema) -> Document:
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
            await session.commit()
            return document

    async def add_embedding(self, embedding_data: dict) -> Embedding:
        async with self.async_session_maker() as session:
            embedding = Embedding(
                doc_id=embedding_data["doc_id"],
                collection_id=embedding_data["collection_id"],
                text=embedding_data["text"],
                embedding=embedding_data["embedding"],
            )
            session.add(embedding)
            await session.commit()
            return embedding

    async def retrieve_docs(self, request: str) -> list[DocumentSchema]:
        async with async_session_maker() as session:
            request_embedding = [1, 2, 3]
            query = (
                select(
                    Embedding.doc_id,
                    (1 - Embedding.embedding.cosine_distance(request_embedding)).label("cosine_similarity"),
                )
                .order_by("cosine_similarity")
                .limit(5)
            )

            result = await session.execute(query)
            print(result)

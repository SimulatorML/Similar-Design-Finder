from sentence_transformers import SentenceTransformer

from src.routers.schemas import DocumentSchema
from src.services.postgres import Postgres


class Repository:
    def __init__(self, postgres: Postgres, collection_name: str, model_name: str) -> None:
        self.postgres = postgres

        self.collection_name = collection_name
        self.model_name = model_name

        self.model = SentenceTransformer(self.model_name)

    @classmethod
    async def create(cls, collection_name: str, model_name: str) -> "Repository":  # noqa: ANN102
        postgres = await Postgres.create(collection_name=collection_name, model_name=model_name)
        return cls(postgres, collection_name=collection_name, model_name=model_name)

    async def add_document(self, doc_data: DocumentSchema) -> None:
        text_for_embedding = "\n".join(
            [
                doc_data.industry or "",
                doc_data.title or "",
                doc_data.description or "",
                doc_data.summarization or "",
                doc_data.tags or "",
            ]
        )
        if not text_for_embedding.strip():
            raise ValueError("Cannot create embedding: text for embedding is empty.")

        embedding_vector = self.model.encode(text_for_embedding).tolist()

        embedding_data = {
            "doc_id": doc_data.doc_id,
            "text": text_for_embedding,
            "embedding": embedding_vector,
        }

        await self.postgres.add_document(doc_data, embedding_data)

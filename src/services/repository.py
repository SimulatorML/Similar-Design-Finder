from abc import ABC, abstractmethod

from sentence_transformers import SentenceTransformer

from src.routers.schemas import DocumentSchema
from src.services.postgres import Postgres

COLLECTION_NAME = "design_docs"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # just for example


class AbstractRepository(ABC):
    @abstractmethod
    async def add_doc(self, doc_data: DocumentSchema) -> None:
        raise NotImplementedError


class Repository(AbstractRepository):
    def __init__(self) -> None:
        self.collection_name = COLLECTION_NAME
        self.model_name = EMBEDDING_MODEL_NAME

        self.postgres = Postgres()
        self.model = SentenceTransformer(self.model_name)

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

        collection = await self.postgres.get_or_create_collection(name=self.collection_name, model=self.model_name)

        document = await self.postgres.add_document(doc_data)

        embedding_data = {
            "doc_id": document.doc_id,
            "collection_id": collection.collection_id,
            "text": text_for_embedding,
            "embedding": embedding_vector,
        }

        await self.postgres.add_embedding(embedding_data)

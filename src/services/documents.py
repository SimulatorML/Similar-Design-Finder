import uuid

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from src.repositories import CollectionRepository, DocsRepository
from src.routers.schemas import DocumentSchema


class DocumentsService:
    def __init__(self, collection_name: str, model_name: str, model_cache_dir: str) -> None:
        self.model_name = model_name
        self.collection_name = collection_name
        self.model_cache_dir = model_cache_dir

        self.model = SentenceTransformer(self.model_name, cache_folder=self.model_cache_dir)

        self.docs_repository = DocsRepository()
        self.collection_repository = CollectionRepository()

    async def add_documents(self, docs_data: list[DocumentSchema]) -> None:
        collection = await self.collection_repository.get_or_create_collection(
            name=self.collection_name, model=self.model_name
        )

        for doc_data in tqdm(docs_data):
            await self._add_document(collection_id=collection.collection_id, doc_data=doc_data)

    async def add_document(self, doc_data: DocumentSchema) -> bool:
        collection = await self.collection_repository.get_or_create_collection(
            name=self.collection_name, model=self.model_name
        )

        await self._add_document(collection_id=collection.collection_id, doc_data=doc_data)

    async def _add_document(self, collection_id: uuid.UUID, doc_data: DocumentSchema) -> None:
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
            "collection_id": collection_id,
            "text": text_for_embedding,
            "embedding": embedding_vector,
        }

        await self.docs_repository.add_document(doc_data=doc_data, embedding_data=embedding_data)

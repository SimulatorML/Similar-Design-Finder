import logging
import uuid

from sentence_transformers import SentenceTransformer

from src.repositories import CollectionRepository, DocsRepository
from src.routers.schemas import Feedback, FinderResult, FindRequest

logger = logging.getLogger(__name__)


class FinderService:
    def __init__(
        self,
        collection_name: str,
        model_name: str,
        model_cache_dir: str,
        collection_repository: CollectionRepository,
        docs_repository: DocsRepository,
    ) -> None:
        self.collection_name = collection_name
        self.model_name = model_name
        self.model_cache_dir = model_cache_dir

        self.collection_repository = collection_repository
        self.docs_repository = docs_repository

        self.model = SentenceTransformer(self.model_name, cache_folder=self.model_cache_dir)

    async def find(self, payload: FindRequest) -> FinderResult:
        query_id = uuid.uuid4()
        request_embedding = self.model.encode(payload.request).tolist()

        collection = await self.collection_repository.get_or_create_collection(
            name=self.collection_name, model=self.model_name
        )

        doc_ids, similarities = await self.docs_repository.get_similarities(
            request_embedding=request_embedding, collection_id=collection.collection_id
        )

        docs = await self.docs_repository.query_similar_docs(doc_ids=doc_ids, similarities=similarities)

        # TODO: Add to database
        logger.info(f"Query: {payload.request}")
        logger.info(f"Found {len(docs)} similar documents")

        return FinderResult(query_id=query_id, request=payload.request, documents=docs)

    async def process_feedback(self, payload: Feedback) -> None:
        pass

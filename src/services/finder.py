import logging
import time
import uuid

from fastapi import HTTPException, status
from sentence_transformers import SentenceTransformer

from src.database.models import FinderQuery, FinderQueryDocument, User
from src.repositories import CollectionRepository, DocsRepository, UserActivityRepository, UserRepository
from src.routers.schemas import Feedback, FinderResult, FindRequest, Source

logger = logging.getLogger(__name__)


class FinderService:
    def __init__(
        self,
        collection_name: str,
        model_name: str,
        model_cache_dir: str,
        collection_repository: CollectionRepository,
        docs_repository: DocsRepository,
        users_repository: UserRepository,
        user_activity_repository: UserActivityRepository,
    ) -> None:
        self.collection_name = collection_name
        self.model_name = model_name
        self.model_cache_dir = model_cache_dir

        self.collection_repository = collection_repository
        self.docs_repository = docs_repository
        self.users_repository = users_repository
        self.user_activity_repository = user_activity_repository

        self.model = SentenceTransformer(self.model_name, cache_folder=self.model_cache_dir)

    async def find(self, payload: FindRequest) -> FinderResult:
        query_id = uuid.uuid4()
        user: User | None = None
        start_time = time.time()

        if payload.source == Source.telegram:
            user = await self.users_repository.get_user_by_id(payload.user_id, telegram=True)
        else:
            user = await self.users_repository.get_user_by_id(payload.user_id)

        if user is None:
            logger.error(f"User with ID {payload.user_id} not found.")
            return FinderResult(query_id=query_id, request=payload.request, documents=[])

        request_embedding = self.model.encode(payload.request).tolist()

        collection = await self.collection_repository.get_or_create_collection(
            name=self.collection_name, model=self.model_name
        )

        doc_ids, similarities = await self.docs_repository.get_similarities(
            request_embedding=request_embedding, collection_id=collection.collection_id
        )

        docs = await self.docs_repository.query_similar_docs(doc_ids=doc_ids, similarities=similarities)

        response_time = int((time.time() - start_time) * 1000)  # milliseconds

        finder_query = FinderQuery(
            query_id=query_id,
            user_id=user.user_id,
            query=payload.request,
            response=str(docs),
            response_time=response_time,
            metadata_info=None,
            feedback=None,
        )
        query_success = await self.user_activity_repository.log_query(finder_query)

        if query_success is None:
            logger.error(f"Failed to log query for user {user.user_id}")

        query_document_entries = [
            FinderQueryDocument(query_id=query_id, doc_id=doc_id, rank=rank)
            for rank, doc_id in enumerate(doc_ids, start=1)
        ]
        docs_success = await self.user_activity_repository.log_query_documents(
            query_document_entries=query_document_entries
        )

        if docs_success is None:
            logger.error(f"Failed to log query documents for query ID {query_id}")

        return FinderResult(query_id=query_id, request=payload.request, documents=docs)

    async def process_feedback(self, payload: Feedback) -> None:
        finder_query = await self.user_activity_repository.update_query_feedback(
            query_id=payload.query_id, feedback=payload.label.value
        )

        if finder_query is None:
            logger.error(f"Failed to update feedback for query ID {payload.query_id}")

        return finder_query

    async def retrieve_query_results(self, query_id: uuid.UUID) -> FinderResult:
        query = await self.user_activity_repository.get_query_by_id(query_id)
        if query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")

        doc_ids = [doc.doc_id for doc in await self.user_activity_repository.get_query_documents(query_id)]
        docs = await self.docs_repository.query_similar_docs(doc_ids=doc_ids)

        return FinderResult(query_id=query_id, request=query.query, documents=docs)

from sentence_transformers import SentenceTransformer

from src.repositories import CollectionRepository, DocsRepository
from src.routers.schemas import DocumentSchema, FinderResult, FindRequest


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
        request_embedding = self.model.encode(payload.request).tolist()

        collection = await self.collection_repository.get_or_create_collection(
            name=self.collection_name, model=self.model_name
        )

        doc_ids, similarities = await self.docs_repository.get_similarities(
            request_embedding=request_embedding, collection_id=collection.collection_id
        )

        docs = await self.docs_repository.query_similar_docs(doc_ids=doc_ids, similarities=similarities)
        response = self._prepare_response(docs)

        # TODO: Add to database

        return FinderResult(request=payload.request, response=response, documents=docs)

    def _prepare_response(self, docs: list[DocumentSchema]) -> str:
        response_lines = []
        for doc in docs:
            line = (
                f"*Company*: {doc.company}\n"
                f"*Industry*: {doc.industry}\n"
                f"*Description*: {doc.description}\n"
                f"*Tags*: {doc.tags}\n"
                f"[Read More]({doc.s3_link})"
            )
            response_lines.append(line)

        return "\n\n---\n\n".join(response_lines)

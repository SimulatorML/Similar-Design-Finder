from sentence_transformers import SentenceTransformer

from src.routers.schemas import FinderResult, FindRequest
from src.services.postgres import Postgres

COLLECTION_NAME = "design_docs"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # just for example


class Finder:
    def __init__(self, postgres: Postgres, collection_name: str, model_name: str) -> None:
        self.postgres = postgres

        self.collection_name = collection_name
        self.model_name = model_name

        self.model = SentenceTransformer(self.model_name)

    @classmethod
    async def create(cls, collection_name: str, model_name: str) -> "Finder":  # noqa: ANN102
        postgres = await Postgres.create(collection_name=collection_name, model_name=model_name)
        return cls(postgres, collection_name=collection_name, model_name=model_name)

    async def find(self, payload: FindRequest) -> FinderResult:
        request_embedding = self.model.encode(payload.request).tolist()
        docs = await self.postgres.retrieve_docs(request_embedding)

        # TODO: Add to database

        return FinderResult(request=payload.request, response="Found documents", documents=docs)

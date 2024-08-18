"""Script for initial filling DB with docs"""

import asyncio
from uuid import uuid4

import pandas as pd

from src.config import settings
from src.repositories import CollectionRepository, DocsRepository
from src.routers.schemas import DocumentSchema
from src.services.documents import DocumentsService

CSV_PATH = "data/raw/evidently_table.csv"


async def populate_database() -> None:
    df = pd.read_csv(CSV_PATH)

    documents_service = DocumentsService(
        collection_name=settings.COLLECTION_NAME,
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_cache_dir=settings.MODEL_CACHE_DIR,
        collection_repository=CollectionRepository(),
        docs_repository=DocsRepository(),
    )

    print("Populating database...")

    docs_data = []
    for index, row in df.iterrows():
        existing_doc = await documents_service.get_document_by_link(row["Link"])

        if existing_doc is not None:
            print(f"Document with link {row['Link']} already exists. Skipping...")
            continue

        doc_data = DocumentSchema(
            doc_id=uuid4(),
            company=row.get("Company"),
            industry=row.get("Industry"),
            title=row.get("Title"),
            description=row.get("Short Description (< 5 words)"),
            summarization=None,
            tags=row.get("Tag"),
            year=row.get("Year"),
            source="Evidently AI",
            status=None,
            s3_link=row["Link"],
            score=0.0,
            metadata=None,
        )
        docs_data.append(doc_data)

    await documents_service.add_documents(docs_data=docs_data)


if __name__ == "__main__":
    asyncio.run(populate_database())

"""Script for initial filling DB with docs"""

import asyncio
from uuid import uuid4

import pandas as pd

from src.config import settings
from src.routers.schemas import DocumentSchema
from src.services.documents import DocumentsService

CSV_PATH = "data/raw/evidently_table.csv"


async def populate_database() -> None:
    df = pd.read_csv(CSV_PATH)

    documents_service = DocumentsService(
        collection_name=settings.COLLECTION_NAME, model_name=settings.EMBEDDING_MODEL_NAME
    )

    print("Populating database...")

    docs_data = []
    for index, row in df.iterrows():
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

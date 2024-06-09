"""Script for initial filling DB with docs"""

import asyncio
from uuid import uuid4

import pandas as pd
from tqdm import tqdm

from src.config import settings
from src.routers.schemas import DocumentSchema
from src.services.repository import Repository

# Определяем путь к вашему CSV файлу
CSV_PATH = "data/raw/evidently_table.csv"


async def populate_database() -> None:
    df = pd.read_csv(CSV_PATH)

    repository = await Repository.create(
        collection_name=settings.COLLECTION_NAME, model_name=settings.EMBEDDING_MODEL_NAME
    )

    print("Populating database...")

    for index, row in tqdm(df.iterrows()):
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

        await repository.add_document(doc_data)


if __name__ == "__main__":
    asyncio.run(populate_database())

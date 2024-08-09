import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.database.models import Collection

logger = logging.getLogger(__name__)


class CollectionRepository:
    @staticmethod
    async def get_or_create_collection(name: str, model: str) -> Collection:
        async with async_session_maker() as session:
            try:
                collection = await session.execute(select(Collection).where(Collection.name == name))
                collection = collection.scalar()

                if not collection:
                    collection = Collection(
                        name=name,
                        model=model,
                    )
                    session.add(collection)
                    await session.commit()

                return collection
            except IntegrityError as exp:
                await session.rollback()
                logger.error(f"Integrity error during getting or creating collection: {exp}")
                return None
            except Exception as exp:
                logger.error(f"Failed to get or create collection: {exp}")
                return None

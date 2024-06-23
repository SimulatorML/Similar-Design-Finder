from sqlalchemy import select

from src.database import async_session_maker
from src.database.models import Collection


class CollectionRepository:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def get_or_create_collection(name: str, model: str) -> Collection:
        async with async_session_maker() as session:
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

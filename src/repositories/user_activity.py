import logging
import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.database.models import FinderQuery, FinderQueryDocument, QueryClick

logger = logging.getLogger(__name__)


class UserActivityRepository:
    async def log_query(self, finder_query: FinderQuery) -> bool:
        async with async_session_maker() as session:
            try:
                session.add(finder_query)
                await session.commit()
                return finder_query
            except IntegrityError as e:
                logger.error(f"Integrity error during query documents logging: {e}")
                await session.rollback()
                return None
            except Exception as e:
                logger.error(f"Failed to log query: {e}")
                return None

    async def log_query_documents(self, query_document_entries: list[FinderQueryDocument]) -> bool:
        async with async_session_maker() as session:
            try:
                for entry in query_document_entries:
                    session.add(entry)
                await session.commit()
                return query_document_entries
            except IntegrityError as e:
                logger.error(f"Integrity error during query documents logging: {e}")
                await session.rollback()
                return None
            except Exception as e:
                logger.error(f"Failed to log query documents: {e}")
                return None

    async def log_click(self, click: QueryClick) -> bool:
        async with async_session_maker() as session:
            try:
                session.add(click)
                await session.commit()
                return click
            except IntegrityError as e:
                logger.error(f"Integrity error during query documents logging: {e}")
                await session.rollback()
                return None
            except Exception as e:
                logger.error(f"Failed to log click: {e}")
                return None

    async def update_query_feedback(self, query_id: uuid.UUID, feedback: str) -> bool:
        async with async_session_maker() as session:
            try:
                result = await session.execute(select(FinderQuery).where(FinderQuery.query_id == query_id))
                finder_query: FinderQuery = result.scalars().first()
                if not finder_query:
                    logger.error(f"Query ID {query_id} not found for feedback update.")
                    return False

                finder_query.feedback = feedback
                session.add(finder_query)
                await session.commit()
                return finder_query
            except IntegrityError as e:
                logger.error(f"Integrity error during feedback update: {e}")
                await session.rollback()
                return None
            except Exception as e:
                logger.error(f"Failed to update feedback: {e}")
                return None

    async def get_query_by_id(self, query_id: uuid.UUID) -> FinderQuery:
        async with async_session_maker() as session:
            query = await session.execute(select(FinderQuery).where(FinderQuery.query_id == query_id))
            return query.scalars().first()

    async def get_query_documents(self, query_id: uuid.UUID) -> list[FinderQueryDocument]:
        async with async_session_maker() as session:
            query = await session.execute(select(FinderQueryDocument).where(FinderQueryDocument.query_id == query_id))
            return query.scalars().all()

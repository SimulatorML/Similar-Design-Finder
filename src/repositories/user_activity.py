import logging
import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.database.models import FinderQueries, FinderQueryDocument, QueriesClicks

logger = logging.getLogger(__name__)


class UserActivityRepository:
    async def log_query(self, finder_query: FinderQueries) -> bool:
        try:
            async with async_session_maker() as session:
                session.add(finder_query)
                await session.commit()
                return True
        except IntegrityError as e:
            logger.error(f"Integrity error during query documents logging: {e}")
            await session.rollback()
            return False
        except Exception as e:
            logger.error(f"Failed to log query: {e}")
            return False

    async def log_query_documents(self, query_document_entries: list[FinderQueryDocument]) -> bool:
        try:
            async with async_session_maker() as session:
                for entry in query_document_entries:
                    session.add(entry)
                await session.commit()
                return True
        except IntegrityError as e:
            logger.error(f"Integrity error during query documents logging: {e}")
            await session.rollback()
            return False
        except Exception as e:
            logger.error(f"Failed to log query documents: {e}")
            return False

    async def log_click(self, click: QueriesClicks) -> bool:
        try:
            async with async_session_maker() as session:
                session.add(click)
                await session.commit()
                return True
        except IntegrityError as e:
            logger.error(f"Integrity error during query documents logging: {e}")
            await session.rollback()
            return False
        except Exception as e:
            logger.error(f"Failed to log click: {e}")
            return False

    async def update_query_feedback(self, query_id: uuid.UUID, feedback: str) -> bool:
        try:
            async with async_session_maker() as session:
                result = await session.execute(select(FinderQueries).where(FinderQueries.query_id == query_id))
                finder_query = result.scalars().first()
                if not finder_query:
                    logger.error(f"Query ID {query_id} not found for feedback update.")
                    return False

                finder_query.feedback = feedback
                session.add(finder_query)
                await session.commit()
                return True
        except IntegrityError as e:
            logger.error(f"Integrity error during feedback update: {e}")
            await session.rollback()
            return False
        except Exception as e:
            logger.error(f"Failed to update feedback: {e}")
            return False

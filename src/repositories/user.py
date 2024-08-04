import logging
import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.database.models import Role, User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self) -> None:
        pass

    async def create_user(self, user: User) -> User:
        async with async_session_maker() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError as exp:
                await session.rollback()
                logger.error(f"Integrity error during user creation: {exp}")
                return None
            except Exception as exp:
                logger.error(f"Failed to create user: {exp}")
                return None

    async def user_exists(self, telegram_id: int) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = result.scalars().first()
            return bool(user)

    async def get_role_by_name(self, role_name: str) -> Role:
        async with async_session_maker() as session:
            result = await session.execute(select(Role).where(Role.role_name == role_name))
            return result.scalars().first()

    async def add_role(self, role: Role) -> Role:
        async with async_session_maker() as session:
            try:
                session.add(role)
                await session.commit()
                await session.refresh(role)
                return role
            except IntegrityError as exp:
                await session.rollback()
                logger.error(f"Integrity error during role creation: {exp}")
                raise ValueError("Role with this name already exists") from exp

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            return result.scalars().first()

import logging
import uuid

from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.database.models import Role, User
from src.routers.schemas import RoleSchema, UserCreateSchema

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self) -> None:
        pass

    async def register(self, user_data: UserCreateSchema) -> User:
        try:
            async with async_session_maker() as session:
                if user_data.password:
                    hashed_password = bcrypt.hash(user_data.password)
                else:
                    hashed_password = None

                user = User(
                    user_id=uuid.uuid4(),
                    telegram_id=user_data.telegram_id,
                    username=user_data.username,
                    email=user_data.email,
                    hashed_password=hashed_password,
                    role_id=0,
                    is_active=True,
                )
                session.add(user)
                await session.commit()
                return user
        except Exception as exp:
            logger.error(f"Failed to register user: {exp}")
            return None

    async def role_exists(self, role_name: str) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(select(Role).where(Role.role_name == role_name))
            role = result.scalars().first()
            return bool(role)

    async def add_role(self, role_data: RoleSchema) -> Role:
        new_role = Role(**role_data.model_dump())
        async with async_session_maker() as session:
            try:
                session.add(new_role)
                await session.commit()
                await session.refresh(new_role)
            except IntegrityError as exp:
                await session.rollback()
                raise ValueError("Role with this name already exists") from exp
        return new_role

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            return result.scalars().first()

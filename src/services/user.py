import logging
import uuid

from passlib.hash import bcrypt

from src.database.models import Role, User
from src.repositories.user import UserRepository
from src.routers.schemas import RoleSchema, UserCreateSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def register(self, payload: UserCreateSchema) -> User | None:
        if payload.telegram_id and await self.user_repository.user_exists(payload.telegram_id):
            logger.info(f"User with telegram_id {payload.telegram_id} already exists.")
            return None

        role: Role = await self.user_repository.get_role_by_name("user")
        if not role:
            logger.error("Role 'user' does not exist in the database.")
            return None

        hashed_password = bcrypt.hash(payload.password) if payload.password else None

        user = User(
            user_id=uuid.uuid4(),
            telegram_id=payload.telegram_id,
            username=payload.username,
            email=payload.email,
            hashed_password=hashed_password,
            role_id=role.role_id,
            is_active=True,
        )

        return await self.user_repository.create_user(user)

    async def ensure_role_exists(self, role_data: RoleSchema) -> None:
        try:
            if not await self.user_repository.get_role_by_name(role_data.role_name):
                role = Role(**role_data.model_dump())
                await self.user_repository.add_role(role)
                logger.info(f"Created new role: {role.role_name} with id: {role.role_id}")
            else:
                logger.info(f"Role already exists: {role_data.role_name}")
        except Exception as exp:
            logger.error(f"Error ensuring role exists: {exp}")
            raise

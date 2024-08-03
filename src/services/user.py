import logging

from src.repositories.user import UserRepository
from src.routers.schemas import RoleSchema, UserCreateSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, payload: UserCreateSchema) -> None:
        pass

    async def ensure_role_exists(self, role_data: RoleSchema) -> None:
        try:
            if not await self.user_repository.role_exists(role_name=role_data.role_name):
                role = await self.user_repository.add_role(role_data=role_data)
                logger.info(f"Created new role: {role.role_name} with id: {role.role_id}")
            else:
                logger.info(f"Role already exists: {role_data.role_name}")
        except Exception as exp:
            logger.error(f"Error ensuring role exists: {exp}")
            raise

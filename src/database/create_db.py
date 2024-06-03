import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from src.database import Base
from src.database.models import *

async def init_db():
    print(f"Database URI: {settings.database_uri}")  # Print the database URI
    engine = create_async_engine(settings.database_uri, echo=True)
    async with engine.begin() as conn:
        # Print info about the tables 
        for table in Base.metadata.tables:
            print(f"Creating table: {table}")
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())

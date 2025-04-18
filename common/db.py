
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from contextlib import asynccontextmanager
import os 
from common.logger import logger

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def provision_database_schema():
    async with engine.begin() as conn:
        import common.models as models
        logger.info("Provisioning the Models")
        await conn.run_sync(models.GenericBase.metadata.create_all)
        logger.info("Models Provisioned")


# This is a very nice pattern that allows dependency injection in fastAPI.
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# This is just in case we want to use session as a context manager
@asynccontextmanager
async def session_context() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def data_exists() -> bool:
    from common.models import CarMake
    async with session_context() as session:
        stmt = select(CarMake).limit(1)
        result = await session.scalar(stmt)
        return result is not None

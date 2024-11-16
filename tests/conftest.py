import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from src.database import get_async_session
from src.config import settings
from src.main import app

#TODO Сделать синхронный движок + синхронную сессию
engine_test = create_async_engine(settings.TEST_DATABASE_URL, echo=True, poolclass=NullPool)
async_session_test = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session
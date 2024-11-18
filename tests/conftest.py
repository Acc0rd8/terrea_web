import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from src.database import get_async_session
from src.config import settings
from src.main import app


engine_test = create_engine(settings.TEST_SYNC_DATABASE_URL, echo=True)
session_test = sessionmaker(engine_test, expire_on_commit=True)


async_engine_test = create_async_engine(settings.TEST_ASYNC_DATABASE_URL, echo=True)
async_session_test = async_sessionmaker(async_engine_test,expire_on_commit=False)


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session
        

app.dependency_overrides[get_async_session] = get_async_session_test
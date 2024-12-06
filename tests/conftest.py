from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.config import settings


engine_test = create_engine(settings.TEST_SYNC_DATABASE_URL, echo=True)
session_test = sessionmaker(engine_test, expire_on_commit=True)


async_engine_test = create_async_engine(settings.TEST_ASYNC_DATABASE_URL, echo=True)
async_session_test = async_sessionmaker(async_engine_test,expire_on_commit=False)

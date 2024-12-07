from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

from src.database import get_async_session
from src.config import settings
from src.main import app


engine_test = create_async_engine(settings.TEST_DATABASE_URL, echo=True)
async_session_factory_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=True)


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory_test() as session:
        try:
            yield session
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            
app.dependency_overrides[get_async_session] = get_async_session_test
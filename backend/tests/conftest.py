from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database import get_async_session
from src.main import app
from src.logger import logger

engine_test = create_async_engine(settings.TEST_DATABASE_URL, echo=False, poolclass=NullPool)
async_session_factory_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory_test() as session:
        try:
            yield session
        except Exception as e:
            '''
            If any exceptions, there will be showing database info in Logs
            '''
            msg = f'Database connection Error {e}'
            extra = {
                'DB_USER_TEST': settings.TEST_DATABASE_INFO['DB_USER_TEST'],
                'DB_PASS_TEST': settings.TEST_DATABASE_INFO['DB_PASS_TEST'],
                'DB_HOST_TEST': settings.TEST_DATABASE_INFO['DB_HOST_TEST'],
                'DB_PORT_TEST': settings.TEST_DATABASE_INFO['DB_PORT_TEST'],
                'DB_NAME_TEST': settings.TEST_DATABASE_INFO['DB_NAME_TEST'],
            }
            logger.critical(msg=msg, extra=extra, exc_info=False)
            await session.rollback() # Rollback SQL transations
            raise
        finally:
            await session.close() # Close session
            
app.dependency_overrides[get_async_session] = get_async_session_test
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings
from src.logger import logger


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self) -> dict:
        cols = []
        for index, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or index < self.repr_cols_num:
                cols.append(f'{col} = {getattr(self, col)}')
        return f'<{self.__class__.__name__}: {', '.join(cols)}>'


engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except:
            msg = 'Database connection Error'
            extra = {
                'DB_USER': settings.DATABASE_INFO['DB_USER'],
                'DB_PASS': settings.DATABASE_INFO['DB_PASS'],
                'DB_HOST': settings.DATABASE_INFO['DB_HOST'],
                'DB_PORT': settings.DATABASE_INFO['DB_PORT'],
                'DB_NAME': settings.DATABASE_INFO['DB_NAME'],
            }
            logger.critical(msg=msg, extra=extra)
            await session.rollback()
            raise
        finally:
            await session.close()
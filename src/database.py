from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from src.config import settings


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        cols = []
        for index, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or index < self.repr_cols_num:
                cols.append(f'{col} = {getattr(self, col)}')
        return f'<{self.__class__.__name__}: {', '.join(cols)}>'


engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

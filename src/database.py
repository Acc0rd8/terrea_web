from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


class Base(DeclarativeBase):
    pass


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=True)


async def get_async_session():
    async with async_session() as session:
        yield session

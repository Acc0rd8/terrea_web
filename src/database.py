from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings
from src.logger import logger


class Base(DeclarativeBase):
    """
    Base Database model class
    
    repr_cols_num - amount columns to print
    repr_cols - additional columns except 'repr_cols_num'

    """    
    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self) -> dict:
        """
        Show model in cmd
        
        Returns:
            string: <'Class.name': 'column1, column2, ...'>
        """        
        cols = []
        for index, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or index < self.repr_cols_num:
                cols.append(f'{col} = {getattr(self, col)}')
        return f'<{self.__class__.__name__}: {', '.join(cols)}>'
    
    @classmethod
    def to_string(cls):
        """
        Tablename to string
        Returns:
            string: Class.tablename
        """        
        return cls.__tablename__.capitalize()


engine = create_async_engine(settings.DATABASE_URL, echo=False) # Creating engine for connection with database settings (DATABASE_URL), echo=True - show SQL transactions
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False) # Async session for creating SQL transations, autoflush=False - don't auto commit


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            '''
            If any exceptions, there will be showing database info in Logs
            '''
            msg = f'Database connection Error {e}'
            extra = {
                'DB_USER': settings.DATABASE_INFO['DB_USER'],
                'DB_PASS': settings.DATABASE_INFO['DB_PASS'],
                'DB_HOST': settings.DATABASE_INFO['DB_HOST'],
                'DB_PORT': settings.DATABASE_INFO['DB_PORT'],
                'DB_NAME': settings.DATABASE_INFO['DB_NAME'],
            }
            logger.critical(msg=msg, extra=extra, exc_info=False)
            await session.rollback() # Rollback SQL transations
            raise
        finally:
            await session.close() # Close session
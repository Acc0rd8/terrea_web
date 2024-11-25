from sqlalchemy import insert, select, update, delete
from abc import ABC, abstractmethod
from pydantic import BaseModel

from src.database import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError
    
    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all():
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None
    
    async def create_one(self, data: dict) -> dict:
        async with async_session() as session:
            stmt = insert(self.model).values(**data)
            await session.execute(stmt)
            await session.commit()
            return {'message': f'{self.model} has been created'}
        
    async def get_one(self, **filter):
        async with async_session() as session:
            query = select(self.model).filter_by(**filter)
            result = await session.execute(query)
            res = result.scalar()
            return res
    
    async def update_one(self, new_data: BaseModel, **filter):
        async with async_session() as session:
            new_dict_data = new_data.model_dump(exclude_unset=True)
            stmt = update(self.model).filter_by(**filter).values(new_dict_data).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            res = result.scalar()
            return res
    
    async def delete_one(self, **filter) -> dict:
        async with async_session() as session:
            stmt = delete(self.model).filter_by(**filter)
            await session.execute(stmt)
            await session.commit()
            return {'message': f'{self.model} has been deleted'}
    
    async def delete_all(self) -> dict:
        async with async_session() as session:
            stmt = delete(self.model)
            await session.execute(stmt)
            await session.commit()
            return {'message': f'All {self.model} have been deleted'}
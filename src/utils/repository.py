from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from pydantic import BaseModel


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
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_one(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data)
        await self.session.execute(stmt)
        await self.session.commit()
        return {'message': f'{self.model} has been created'}
        
    async def get_one(self, **filter):
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        res = result.scalar()
        return res
    
    async def update_one(self, new_data: BaseModel, **filter):
        new_dict_data = new_data.model_dump(exclude_unset=True)
        stmt = update(self.model).filter_by(**filter).values(new_dict_data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        res = result.scalar()
        return res
    
    async def delete_one(self, **filter) -> dict:
        stmt = delete(self.model).filter_by(**filter)
        await self.session.execute(stmt)
        await self.session.commit()
        return {'message': f'{self.model} has been deleted'}
    
    async def delete_all(self) -> dict:
        stmt = delete(self.model)
        await self.session.execute(stmt)
        await self.session.commit()
        return {'message': f'All {self.model} have been deleted'}
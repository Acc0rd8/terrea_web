from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base


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
        return {'message': f'{self.model.to_string()} has been created'}
        
    async def get_one(self, **filter) -> Base:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        res = result.scalar()
        return res
    
    async def update_one(self, new_data: BaseModel, **filter) -> Base:
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
        return {'message': f'{self.model.to_string()} has been deleted'}
    
    async def delete_all(self) -> dict:
        stmt = delete(self.model)
        await self.session.execute(stmt)
        await self.session.commit()
        return {'message': f'All {self.model.to_string()}s have been deleted'}
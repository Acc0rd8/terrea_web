from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from redis.exceptions import RedisError

from src.database import Base
from src.logger import logger


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(): # INSERT
        raise NotImplementedError
    
    @abstractmethod
    async def get_one(): # SELECT
        raise NotImplementedError
    
    @abstractmethod
    async def update_one(): # UPDATE
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one(): # DELETE
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all(): # DELETE
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model: Base = None # Choose Base Model
    
    def __init__(self, session: AsyncSession):
        self.session = session # Take async session
    
    async def create_one(self, data: dict) -> dict:
        try:
            stmt = insert(self.model).values(**data)
            await self.session.execute(stmt)
            await self.session.commit()
            return {'message': f'{self.model.to_string()} has been created'}
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.critical(msg='SQLALCHEMY CRITICAL ERROR', extra={'Error': e}, exc_info=False) # log
            raise SQLAlchemyError
        
    async def get_one(self, **filter) -> Base:
        try:
            query = select(self.model).filter_by(**filter)
            result = await self.session.execute(query)
            res = result.scalar()
            return res
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.critical(msg='SQLALCHEMY CRITICAL ERROR', extra={'Error': e}, exc_info=False) # log
            raise SQLAlchemyError
    
    async def update_one(self, new_data: BaseModel, **filter) -> Base:
        try:
            new_dict_data = new_data.model_dump(exclude_unset=True) # Converting Pydantic model to dict with excluding unset fields
            stmt = update(self.model).filter_by(**filter).values(new_dict_data).returning(self.model)
            result = await self.session.execute(stmt)
            await self.session.commit()
            res = result.scalar()
            return res
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.critical(msg='SQLALCHEMY CRITICAL ERROR', extra={'Error': e}, exc_info=False) # log
            raise SQLAlchemyError
    
    async def delete_one(self, **filter) -> dict:
        try:
            stmt = delete(self.model).filter_by(**filter)
            await self.session.execute(stmt)
            await self.session.commit()
            return {'message': f'{self.model.to_string()} has been deleted'}
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.critical(msg='SQLALCHEMY CRITICAL ERROR', extra={'Error': e}, exc_info=False) # log
            raise SQLAlchemyError
    
    async def delete_all(self) -> dict:
        try:
            stmt = delete(self.model)
            await self.session.execute(stmt)
            await self.session.commit()
            return {'message': f'All {self.model.to_string()}s have been deleted'}
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.critical(msg='SQLALCHEMY CRITICAL ERROR', extra={'Error': e}, exc_info=False) # log
            raise SQLAlchemyError
        

class RedisRepository(AbstractRepository):
    data_type = None
    
    def __init__(self, RedisServer: Redis):
        self.redis = RedisServer
        
    async def create_one(self, *data) -> dict:
        try:
            if self.data_type == 'string':
                await self.redis.set(name=data[0], value=data[1])
            elif self.data_type == 'hash':
                await self.redis.hset(name=data[0], key=data[1], value=data[2])
            else:
                raise TypeError  #TODO
            
            return {'success': True}
        except RedisError as e:
            msg = 'REDIS CRITICAL ERROR'
            extra = {'Error': e}
            logger.critical(msg=msg, extra=extra, exc_info=False)  # log
            raise e
    
    async def get_one(self, *data) -> str | dict:
        try:
            if self.data_type == 'string':
                result: bytes = await self.redis.get(name=data[0])
            elif self.data_type == 'hash':
                result: bytes = await self.redis.hget(name=data[0], key=data[1])
            else:
                raise TypeError  #TODO
            
            if result:
                return result.decode('utf-8')
            return None
        except RedisError as e:
            msg = 'REDIS CRITICAL ERROR'
            extra = {'Error': e}
            logger.critical(msg=msg, extra=extra, exc_info=False)  # log
            raise e
    
    async def update_one(self, *data) -> dict:  #TODO
        try:
            if self.data_type == 'string':
                await self.redis.set(name=data[0], value=data[1])
            elif self.data_type == 'hash':
                await self.redis.hset(name=data[0], key=data[1], value=data[2])
            else:
                raise TypeError  #TODO
            
            return {'success': True}
        except RedisError as e:
            msg = 'REDIS CRITICAL ERROR'
            extra = {'Error': e}
            logger.critical(msg=msg, extra=extra, exc_info=False)  # log
            raise e
    
    async def delete_one(self, *data) -> dict:
        try:
            await self.redis.delete(data)
            
            return {'success': True}
        except RedisError as e:
            msg = 'REDIS CRITICAL ERROR'
            extra = {'Error': e}
            logger.critical(msg=msg, extra=extra, exc_info=False)  # log
            raise e
    
    async def delete_all(self) -> dict:
        try:
            await self.redis.flushdb(asynchronous=True)
            
            return {'success': True}
        except RedisError as e:
            msg = 'REDIS CRITICAL ERROR'
            extra = {'Error': e}
            logger.critical(msg=msg, extra=extra, exc_info=False)  # log
            raise e
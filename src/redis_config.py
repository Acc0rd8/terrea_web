import functools

from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.config import settings
from src.dependencies.redis_service import redis_hash_type_service, redis_string_type_service
from src.logger import logger
from src.schemas.base_schema import BaseSchema


class RedisServer:
    def __init__(self, host: str | int, port: int, username=None, password=None, db=0):
        try:
            self.connection = Redis(host=host, port=port, username=username, password=password, db=db)  # Connect to Database
            self.redis_hash_type_service = redis_hash_type_service(self.connection)
            self.redis_string_type_service = redis_string_type_service(self.connection)
        except RedisError as e:
            msg = 'Redis connection error'
            extra = {
                'REDIS_HOST': settings.REDIS_HOST,
                'REDIS_PORT': settings.REDIS_PORT,
            }
            logger.critical(msg=msg, extra=extra, exc_info=True)
            raise RedisError
    
    # TODO!!!
    def cache(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            
            # TODO!!!
            if isinstance(response, BaseSchema):
                dict_response = response.model_dump()
                for key, value in dict_response.items():
                    if isinstance(value, bool):
                        dict_response[key] = str(value)
                
                dict_response.pop('user_tasks')
                dict_response.pop('projects')
                            
                if await self.redis_hash_type_service.get_many(dict_response['username'], dict_response.keys()) is not None:
                    await self.redis_hash_type_service.create_many(dict_response['username'], **dict_response)
                
                info = await self.redis_hash_type_service.get_many(dict_response['username'], dict_response.keys())
                
                # TODO!!!
                index = 0
                for key in dict_response.keys():
                    dict_response[key] = info[index].decode('utf-8')
                    index += 1
                dict_response['projects'] = response.model_dump()['projects']
                dict_response['user_tasks'] = response.model_dump()['user_tasks']
                return dict_response
                    
        return wrapper
        

app_redis = RedisServer(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
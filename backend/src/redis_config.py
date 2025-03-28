import functools
import json

from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.config import settings
from src.dependencies.redis_service import redis_hash_type_service, redis_string_type_service
from src.logger import logger
from src.schemas.user_schemas import UserRead
from src.schemas.project_schemas import ProjectRead


class RedisServer:
    """
    App Redis connection
    
    Fields:
        <self> connection (Redis): Redis connection
        <self> redis_hash_type_service (RedisHashTypeService): Redis service for hash type data
        <self> redis_string_type_service (RedisStringTypeService): Redis service for string type data
    """
    
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
            raise
    
    # TODO!!!
    def cache(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)

            if isinstance(response, UserRead):
                user_dict = response.model_dump()
                
                # Check if User already exists in Redis
                if await self.redis_hash_type_service.get_many(f"user_name:{user_dict["username"]}") is not None:
                    # DEL data
                    await self.redis_hash_type_service.delete_one(f"user_name:{user_dict["username"]}")
                
                # From "date", "datetime" to "str"
                for project in response.projects:
                    project.created_at = str(project.created_at)
                    for project_task in project.project_tasks:
                        project_task.created_at = str(project_task.created_at)
                        project_task.updated_at = str(project_task.updated_at)
                        project_task.deadline = str(project_task.deadline)
                for user_task in response.user_tasks:
                    user_task.created_at = str(user_task.created_at)
                    user_task.updated_at = str(user_task.updated_at)
                    user_task.deadline = str(user_task.deadline)
                user_dict["is_active"] = str(user_dict["is_active"])
                
                # Serialization in JSON
                user_dict["projects"] = json.dumps([project.dict() for project in response.projects])
                user_dict["user_tasks"] = json.dumps([task.dict() for task in response.user_tasks])
                
                # HMSET data
                await self.redis_hash_type_service.create_many(name_val=f"user_name:{user_dict["username"]}", **user_dict)
                
                # HGETALL data
                user_data_temp = await self.redis_hash_type_service.get_many(f"user_name:{user_dict["username"]}")
                
                # Decode binary strings
                user_data = dict()
                for key, value in user_data_temp.items():
                    user_data[key.decode("utf-8")] = value.decode("utf-8")
                
                # Deserialization data
                user_data["projects"] = json.loads(user_data["projects"])
                user_data["user_tasks"] = json.loads(user_data["user_tasks"])
                
                return user_data
            elif isinstance(response, ProjectRead):
                project_dict = response.model_dump()
                
                # Check if Project already exists in Redis
                if await self.redis_hash_type_service.get_many(project_dict["name"]) is not None:
                    # DEL data
                    await self.redis_hash_type_service.delete_one(f"user_name:{project_dict["name"]}")
                
                # From "date", "datetime" to "str"
                for task in response.project_tasks:
                    task.created_at = str(task.created_at)
                    task.updated_at = str(task.updated_at)
                    task.deadline = str(task.deadline)

                # Serialization in JSON
                project_dict["project_tasks"] = json.dumps([project_tasks.dict() for project_tasks in response.project_tasks])
                
                # HMSET data
                await self.redis_hash_type_service.create_many(name_val=f"project_name:{project_dict["name"]}", **project_dict)
            
                # HGETALL data
                project_dict_temp = await self.redis_hash_type_service.get_many(f"project_name:{project_dict["name"]}")
                
                # Decode binary strings
                project_data = dict()
                for key, value in project_dict_temp.items():
                    project_data[key.decode("utf-8")] = value.decode("utf-8")
                
                # Deserialization data
                project_data["project_tasks"] = json.loads(project_data["project_tasks"])
                
                return project_data
            else:
                pass
        return wrapper
        

app_redis = RedisServer(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

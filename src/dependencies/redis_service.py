from redis.asyncio import Redis

from src.redis_repositories.redis_string_type_service import RedisStringTypeService
from src.redis_repositories.redis_hash_type_service import RedisHashTypeService
from src.utils.redis_repos import RedisStringTypeRepository, RedisHashTypeRepository


def redis_string_type_service(connection: Redis):
    return RedisStringTypeService(RedisStringTypeRepository(connection))

def redis_hash_type_service(connection: Redis):
    return RedisHashTypeService(RedisHashTypeRepository(connection))
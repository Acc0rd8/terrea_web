from redis.asyncio import Redis

from src.redis_repositories import RedisStringTypeDAO
from src.redis_repositories import RedisHashTypeDAO
from src.utils.redis_repos import RedisStringTypeRepository, RedisHashTypeRepository


def redis_string_type_dao_dependency(connection: Redis):
    return RedisStringTypeDAO(RedisStringTypeRepository(connection))


def redis_hash_type_dao_dependency(connection: Redis):
    return RedisHashTypeDAO(RedisHashTypeRepository(connection))

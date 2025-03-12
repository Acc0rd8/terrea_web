from src.redis_repositories.redis_string_type import RedisStringTypeService
from src.redis_repositories.redis_hash_type import RedisHashTypeService
from src.utils.redis_repos import RedisStringTypeRepository, RedisHashTypeRepository
from src.redis_config import RedisServer


def redis_string_type_service():
    return RedisStringTypeService(RedisStringTypeRepository(RedisServer))

def redis_hash_type_service():
    return RedisHashTypeService(RedisHashTypeRepository(RedisServer))
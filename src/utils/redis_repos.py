from src.utils.repository import RedisRepository


class RedisStringTypeRepository(RedisRepository):
    data_type = 'string'
    

class RedisHashTypeRepository(RedisRepository):
    data_type = 'hash'
from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.config import settings
from src.logger import logger


try:
    RedisServer = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)  # Connect to Database
except RedisError as e:
    msg = 'Redis connection error'
    extra = {
        'REDIS_HOST': settings.REDIS_HOST,
        'REDIS_PORT': settings.REDIS_PORT,
    }
    logger.critical(msg=msg, extra=extra, exc_info=True)
    raise RedisError
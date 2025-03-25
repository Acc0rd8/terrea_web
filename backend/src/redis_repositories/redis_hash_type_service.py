from src.utils.repository import RedisRepository


class RedisHashTypeService:
    """
    Redis service for hash type data
    
    Fields:
        <self> redis_repo (RedisRepository): Redis hash type repository
    """
    
    def __init__(self, redis_repo: RedisRepository):
        self.redis_repo: RedisRepository = redis_repo
        
    async def create_one(self, name: str, key: str, value: str | int) -> dict:
        result = await self.redis_repo.create_one(name, key, value)
        return result
    
    async def create_many(self, name: str, **data) -> dict:
        result = await self.redis_repo.create_many(name, **data)
        return result
    
    async def get_one(self, name: str, key: str) -> dict:
        result = await self.redis_repo.get_one(name, key)
        return result
    
    async def get_many(self, name: str, *data) -> dict:
        result = await self.redis_repo.get_many(name, *data)
        return result
        
    async def update_one(self, name: str, key: str, value: str | int) -> dict:
        result = await self.redis_repo.update_one(name, key, value)
        return result
    
    async def delete_one(self, name: str) -> dict:
        result = await self.redis_repo.delete_one(name)
        return result
    
    async def delete_all(self) -> dict:
        result = await self.redis_repo.delete_all()
        return result

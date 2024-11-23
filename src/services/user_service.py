from src.schemas.user_schemas import UserCreate, UserUpdate
from src.utils.repository import AbstractRepository
from src.models.model_user import User


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()
        
    async def create_user(self, user: UserCreate) -> dict:
        user_dict = user.model_dump()
        result = await self.user_repo.create_one(user_dict)
        return result
    
    async def get_user(self, user_email: str) -> User:
        result = await self.user_repo.get_one(email=user_email)
        return result
    
    async def update_user(self, new_user: UserUpdate, user_email: str) -> User:
        result = await self.user_repo.update_one(new_data=new_user, email=user_email)
        return result
    
    async def delete_one_user(self, user_email: str) -> dict:
        result = await self.user_repo.del_one(id=user_email)
        return result
    
    async def delete_all_users(self) -> dict:
        result = await self.user_repo.del_all()
        return result
from src.models.model_user import User
from src.schemas.user_schemas import UserCreate, UserUpdate
from src.utils.repository import SQLAlchemyRepository


class UserService:
    def __init__(self, user_repo: SQLAlchemyRepository):
        self.user_repo: SQLAlchemyRepository = user_repo
        
    async def create_user(self, user: UserCreate) -> dict:
        user_dict = user.model_dump() # Converting Pydantic model (UserCreate) to dict
        result = await self.user_repo.create_one(user_dict)
        return result
    
    async def get_user_by_email(self, user_email: str) -> User:
        result = await self.user_repo.get_one(email=user_email)
        return result
    
    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.user_repo.get_one(id=user_id)
        return result
    
    async def get_user_by_name(self, user_name: str) -> User:
        result = await self.user_repo.get_one(username=user_name)
        return result
    
    async def update_user(self, new_user: UserUpdate, user_email: str) -> User:
        result = await self.user_repo.update_one(new_data=new_user, email=user_email)
        return result
    
    async def delete_one_user(self, user_email: str) -> dict:
        result = await self.user_repo.delete_one(email=user_email)
        return result
    
    async def delete_all_users(self) -> dict:
        result = await self.user_repo.delete_all()
        return result
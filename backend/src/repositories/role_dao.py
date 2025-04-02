from src.models import Role
from src.schemas import RoleCreateSchema, RoleUpdateSchema
from src.utils.repository import SQLAlchemyRepository


class RoleDAO:
    """
    Role DAO service
    
    Fields:
        <self> role_repo (SQLAlchemyRepository): Role repository
    """
    
    def __init__(self, role_repo: SQLAlchemyRepository):
        self.role_repo: SQLAlchemyRepository = role_repo
        
    async def create_role(self, role: RoleCreateSchema) -> dict:
        role_dict = role.model_dump() # Converting Pydantic model (RoleCreate) to dict
        result = await self.role_repo.create_one(role_dict)
        return result
    
    async def get_role(self, role_id: int) -> Role:
        result = await self.role_repo.get_one(id=role_id)
        return result
    
    async def update_role(self, new_role: RoleUpdateSchema, role_id: int) -> Role:
        result = await self.role_repo.update_one(new_data=new_role, id=role_id)
        return result
    
    async def delete_one_role(self, role_id: int) -> dict:
        result = await self.role_repo.delete_one(id=role_id)
        return result
    
    async def delete_all_roles(self) -> dict:
        result = await self.role_repo.delete_all()
        return result

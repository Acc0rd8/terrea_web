from src.schemas.role_schemas import RoleCreate, RoleUpdate
from src.utils.repository import AbstractRepository
from src.models.model_role import Role


class RoleService:
    def __init__(self, role_repo: AbstractRepository):
        self.role_repo: AbstractRepository = role_repo()
        
    async def create_role(self, role: RoleCreate) -> dict:
        role_dict = role.model_dump()
        result = await self.role_repo.create_one(role_dict)
        return result
    
    async def get_role(self, role_id: int) -> Role:
        result = await self.role_repo.get_one(id=role_id)
        return result
    
    async def update_role(self, new_role: RoleUpdate, role_id: int) -> Role:
        result = await self.role_repo.update_one(new_data=new_role, id=role_id)
        return result
    
    async def delete_one_role(self, role_id: int) -> dict:
        result = await self.role_repo.del_one(id=role_id)
        return result
    
    async def delete_all_roles(self) -> dict:
        result = await self.role_repo.del_all()
        return result
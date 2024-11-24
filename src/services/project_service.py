from src.schemas.project_schemas import ProjectCreate, ProjectUpdate
from src.utils.repository import AbstractRepository
from src.models.model_project import Project


class ProjectService:
    def __init__(self, project_repo: AbstractRepository):
        self.project_repo: AbstractRepository = project_repo()
        
    async def create_project(self, project: ProjectCreate, user_id: int) -> dict:
        project_dict = project.model_dump()
        project_dict.update({'owner_id': user_id})
        result = await self.project_repo.create_one(project_dict)
        return result
    
    async def get_project_by_id(self, project_id: int) -> Project:
        result = await self.project_repo.get_one(id=project_id)
        return result
    
    async def get_project_by_name(self, project_name: str) -> Project:
        result = await self.project_repo.get_one(name=project_name)
        return result
    
    async def update_project(self, new_project: ProjectUpdate, project_id: int) -> Project:
        result = await self.project_repo.update_one(new_data=new_project, id=project_id)
        return result
    
    async def delete_one_project_by_id(self, project_id: int) -> dict:
        result = await self.project_repo.delete_one(id=project_id)
        return result
    
    async def delete_one_project_by_name(self, project_name: str) -> dict:
        result = await self.project_repo.delete_one(name=project_name)
        return result
    
    async def delete_all_projects(self) -> dict:
        result = await self.project_repo.delete_all()
        return result
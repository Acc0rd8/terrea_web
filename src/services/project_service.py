from src.schemas.project_schemas import ProjectCreate, ProjectUpdate
from src.utils.repository import AbstractRepository
from src.models.model_project import Project


class ProjectService:
    def __init__(self, project_repo: AbstractRepository):
        self.project_repo: AbstractRepository = project_repo()
        
    async def create_project(self, project: ProjectCreate) -> dict:
        project_dict = project.model_dump()
        result = await self.project_repo.create_one(project_dict)
        return result
    
    async def get_project(self, project_id: int) -> Project:
        result = await self.project_repo.get_one(id=project_id)
        return result
    
    async def update_project(self, new_project: ProjectUpdate, project_id: int) -> Project:
        result = await self.project_repo.update_one(new_data=new_project, id=project_id)
        return result
    
    async def delete_one_project(self, project_id: int) -> dict:
        result = await self.project_repo.del_one(id=project_id)
        return result
    
    async def delete_all_projects(self) -> dict:
        result = await self.project_repo.del_all()
        return result
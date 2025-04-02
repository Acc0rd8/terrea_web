from src.models import Project
from src.schemas import ProjectCreateSchema, ProjectUpdateSchema
from src.utils.repository import SQLAlchemyRepository


class ProjectDAO:
    """
    Project DAO service
    
    Fields:
        <self> project_repo (SQLAlchemyRepository): Project repository
    """
    
    def __init__(self, project_repo: SQLAlchemyRepository):
        self.project_repo: SQLAlchemyRepository = project_repo
        
    async def create_project(self, project: ProjectCreateSchema, user_id: int) -> dict:
        project_dict = project.model_dump() # Converting Pydantic model (ProjectCreate) to dict
        project_dict.update({'owner_id': user_id})
        result = await self.project_repo.create_one(project_dict)
        return result
    
    async def get_project_by_id(self, project_id: int) -> Project:
        result = await self.project_repo.get_one(id=project_id)
        return result
    
    async def get_project_by_name(self, project_name: str) -> Project:
        result = await self.project_repo.get_one(name=project_name)
        return result
    
    async def update_project(self, new_project: ProjectUpdateSchema, project_id: int) -> Project:
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

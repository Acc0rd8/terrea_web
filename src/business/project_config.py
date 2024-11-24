from fastapi import HTTPException, status
import re

from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.services.project_service import ProjectService
from src.models.model_user import User


class Project:
    @staticmethod
    async def create_new_project(project_create: ProjectCreate, user_data: User, project_service: ProjectService) -> dict:
        await project_service.create_project(project_create, user_data.id)
        return {'message': 'Проект успешно создан'}
            
    
    #TODO Add the need for access rights to see projects
    @staticmethod
    async def get_some_project_by_name(project_name: str, project_service: ProjectService) -> ProjectRead:
        project = await project_service.get_project_by_name(project_name)
        project_model = ProjectRead.model_validate(project)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{project_model.created_at}')
        project_model.created_at = date[0]
        return project_model
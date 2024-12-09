import re

from fastapi import HTTPException, status

from src.models.model_user import User
from src.repositories.project_service import ProjectService
from src.repositories.task_service import TaskService
from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.schemas.task_schemas import TaskCreate


class ProjectConfig:
    @staticmethod
    async def create_new_project(project_create: ProjectCreate, user_data: User, project_service: ProjectService) -> dict:
        await project_service.create_project(project_create, user_data.id)
        return {'message': 'Project has been created'}
            
    @staticmethod
    async def get_some_project_by_name(project_name: str, user_data: User, project_service: ProjectService) -> ProjectRead:
        project = await project_service.get_project_by_name(project_name)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project doesnt exist'
            )
        if project.owner_id != user_data.id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='You dont have enough access rights to see this project'
            )
        project_model = ProjectRead.model_validate(project)
        date = re.search(r'\d{4}-\d{2}-\d{2}', f'{project_model.created_at}')
        project_model.created_at = date[0]
        return project_model
    
    @staticmethod
    async def delete_current_project(project_name: str, user_data: User, project_service: ProjectService) -> dict:
        project = await project_service.get_project_by_name(project_name)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project doesnt exist'
            )
        
        if project.owner_id != user_data.id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='You dont have enough access rights to see this project'
            )
            
        await project_service.delete_one_project_by_name(project_name)
        return {'message': 'Project has been deleted'}
    
    @staticmethod
    async def create_task_in_current_project(project_name: str, task_create: TaskCreate, user_data: User, task_service: TaskService, project_service: ProjectService) -> dict:
        project = await project_service.get_project_by_name(project_name)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Project doesnt exist'
            )
        if project.owner_id != user_data.id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='You dont have enough access rights to see this project'
            )
            
        await task_service.create_task(task_create, project.id, user_data.id)
        return {'message': 'Task has been created'}
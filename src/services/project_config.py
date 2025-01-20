import re

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from src.models.model_user import User
from src.repositories.project_service import ProjectService
from src.repositories.task_service import TaskService
from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.schemas.task_schemas import TaskCreate
from src.logger import logger
from src.dependencies.security import Security


class ProjectConfig:
    @staticmethod
    async def create_new_project(project_create: ProjectCreate, user_data: User, project_service: ProjectService) -> dict:
        try:
            project_create_dict = project_create.model_dump()
            if await Security.validate_shemas_data_project(project_create_dict):
                for project in user_data.projects:
                    project_dict = ProjectRead.model_validate(project).model_dump()
                    if project_dict['name'] == project_create.name:
                        logger.warning(msg='Project name is already taken', extra={'project_name': project_create.name})
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail='Project name is already taken. Please take new name.'
                        )
                await project_service.create_project(project_create, user_data.id)
                return {'message': 'Project has been created'}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Use only alphabet letters and numbers'
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Server Error'
            )
            
    @staticmethod
    async def get_some_project_by_name(project_name: str, user_data: User, project_service: ProjectService) -> ProjectRead:
        try:
            if Security.validate_path_data(project_name):
                project = await project_service.get_project_by_name(project_name)
                if project is None:
                    msg = 'Project doesnt exist'
                    logger.warning(msg=msg)
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Project doesnt exist'
                    )
                if project.owner_id != user_data.id:
                    msg = 'You dont have enough access rights to see this project'
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra)
                    raise HTTPException(
                        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail='You dont have enough access rights to see this project'
                    )
                project_model = ProjectRead.model_validate(project)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{project_model.created_at}')
                project_model.created_at = date[0]
                return project_model
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Use only alphabet letters and numbers'
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Server Error'
            )
    
    @staticmethod
    async def delete_current_project(project_name: str, user_data: User, project_service: ProjectService) -> dict:
        try:
            if Security.validate_path_data(project_name):
                project = await project_service.get_project_by_name(project_name)
                if project is None:
                    msg = 'Project doesnt exist'
                    logger.warning(msg=msg)
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Project doesnt exist'
                    )
                
                if project.owner_id != user_data.id:
                    msg = 'You dont have enough access rights to see this project'
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra)
                    raise HTTPException(
                        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail='You dont have enough access rights to see this project'
                    )
                    
                await project_service.delete_one_project_by_name(project_name)
                return {'message': 'Project has been deleted'}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Use only alphabet letters and numbers'
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Server Error'
            )
    
    @staticmethod
    async def create_task_in_current_project(project_name: str, task_create: TaskCreate, user_data: User, task_service: TaskService, project_service: ProjectService) -> dict:
        try:
            if Security.validate_path_data(project_name) and Security.validate_schemas_data_task(task_create.model_dump()):
                project = await project_service.get_project_by_name(project_name)
                if project is None:
                    msg = 'Project doesnt exist'
                    logger.warning(msg=msg)
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='Project doesnt exist'
                    )
                if project.owner_id != user_data.id:
                    msg = 'You dont have enough access rights to see this project'
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra)
                    raise HTTPException(
                        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail='You dont have enough access rights to see this project'
                    )
                    
                await task_service.create_task(task_create, project.id, user_data.id)
                return {'message': 'Task has been created'}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Use only alphabet letters and numbers'
                )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Server Error'
            )
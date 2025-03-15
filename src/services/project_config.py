import re

from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from src.exceptions.conflict_error import ConflictError
from src.exceptions.validation_error import ValidationError
from src.exceptions.server_error import ServerError
from src.exceptions.exist_error import ExistError
from src.exceptions.access_error import AccessError
from src.models.model_user import User
from src.repositories.project_service import ProjectService
from src.repositories.task_service import TaskService
from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.schemas.task_schemas import TaskCreate
from src.logger import logger
from src.dependencies.validation_manager import ValidationManager


class ProjectConfig:
    @staticmethod
    async def create_new_project(project_create: ProjectCreate, user_data: User, project_service: ProjectService) -> dict:
        """
        Create new Project

        Args:
            project_create (ProjectCreate): Project data Validation
            user_data (User): User data (SQLAlchemy model)
            project_service (ProjectService): Project DAO service

        Raises:
            ConflictError: status - 409, Project name is already taken
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            dict[str, str | int]: Project has been created 
        """
        try:
            project_create_dict = project_create.model_dump() # Converting Pydantic model to dict
            if await ValidationManager.validate_shemas_data_project(project_create_dict):    # Check User symbols
                for project in user_data.projects:
                    project_dict = ProjectRead.model_validate(project).model_dump() # 1. Converting SQLAlchemy model to Pydantic model (ProjectRead), 2. Converting Pydantic model to dict
                    if project_dict['name'] == project_create.name:
                        msg = 'Project name is already taken'
                        extra = {'project_name': project_create.name}
                        logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                        raise ConflictError(msg='Project name is already taken')
                    
                await project_service.create_project(project_create, user_data.id)
                return {'message': 'Project has been created', 'status_code': status.HTTP_200_OK}
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'project_create_dict': project_create_dict}
                logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
            
    @staticmethod
    async def get_some_project_by_name(project_name: str, user_data: User, project_service: ProjectService) -> ProjectRead:
        """
        Show another User Project

        Args:
            project_name (str): Project name
            user_data (User): User data (SQLAlchemy model)
            project_service (ProjectService): Project DAO service

        Raises:
            ExistError: status - 404, Project doesn't exist
            AccessError: status - 405, Don't have enough access rights to see the project
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            ProjectRead: Project data
        """
        try:
            if ValidationManager.validate_path_data(project_name): # Check User symbold
                project = await project_service.get_project_by_name(project_name) # Searching for a Project in the Database
                if project is None:
                    msg = "Project doesn't exist"
                    logger.warning(msg=msg, exc_info=True)  # log
                    raise ExistError(msg="Project doesn't exist")
                    
                if project.owner_id != user_data.id: # If User doesn't own the project
                    msg = "You don't have enough access rights to see this project"
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                    raise AccessError(msg="You don't have enough access rights to see this project")
                    
                project_model = ProjectRead.model_validate(project) # Converting SQLAlchemy model to Pydantic model (ProjectRead)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{project_model.created_at}') # Date type YYYY-MM-DD
                project_model.created_at = date[0]
                return project_model
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'project_name': project_name}
                logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
    
    @staticmethod
    async def delete_current_project(project_name: str, user_data: User, project_service: ProjectService) -> dict:
        """
        Delete Project

        Args:
            project_name (str): Project name
            user_data (User): User data (SQLAlchemy model)
            project_service (ProjectService): Project DAO service

        Raises:
            ExistError: status - 404, Project doesn't exist
            AccessError: status - 405, Don't have enough access rights to see the project
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            dict[str, str | int]: Project has been deleted
        """
        try:
            if ValidationManager.validate_path_data(project_name): # Check User symbols
                project = await project_service.get_project_by_name(project_name) # Searching for a Project in the Database
                if project is None:
                    msg = "Project doesn't exist"
                    logger.warning(msg=msg, exc_info=True)  # log
                    raise ExistError(msg="Project doesn't exist")
                
                if project.owner_id != user_data.id: # If User doesn't own the project
                    msg = "You don't have enough access rights to see this project"
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                    raise AccessError(msg="You don't have enough access rights to see this project")
                    
                await project_service.delete_one_project_by_name(project_name)
                return {'message': 'Project has been deleted', 'status_code': status.HTTP_200_OK}
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'project_name': project_name}
                logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
    
    @staticmethod
    async def create_task_in_current_project(project_name: str, task_create: TaskCreate, user_data: User, task_service: TaskService, project_service: ProjectService) -> dict:
        """
        Create Task in Project

        Args:
            project_name (str): Project name
            task_create (TaskCreate): Task data Validation
            user_data (User): User data (SQLAlcehmy model)
            task_service (TaskService): Task DAO service
            project_service (ProjectService): Project DAO service

        Raises:
            ExistError: status - 404, Project doesn't exist
            AccessError: status - 405, Don't have enough access rights to see the project
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            dict[str, str | int]: Task has been created
        """
        try:
            if ValidationManager.validate_path_data(project_name) and ValidationManager.validate_schemas_data_task(task_create.model_dump()): # Check User symbols
                project = await project_service.get_project_by_name(project_name) # Searching for a Project in the Database
                if project is None:
                    msg = "Project doesn't exist"
                    logger.warning(msg=msg, exc_info=True)  # log
                    raise ExistError(msg="Project doesn't exist")
                    
                if project.owner_id != user_data.id: # If User doesn't own the project
                    msg = "You don't have enough access rights to see this project"
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                    raise AccessError(msg="You don't have enough access rights to see this project")
                    
                await task_service.create_task(task_create, project.id, user_data.id)
                return {'message': 'Task has been created', 'status_code': status.HTTP_200_OK}
            else:
                msg = 'Use only alphabet letters and numbers'
                extra = {'project_name': project_name}
                logger.warning(msg=msg, extra=extra, exc_info=True)  # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()

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
from src.schemas.response_schema import ResponseSchema
from src.logger import logger
from src.dependencies.validation_manager import ValidationManager


class ProjectConfig:
    """
    Project router service
    
    Fields:
        <self> __project_service (ProjectService): Project DAO service
        <self> __task_service (TaskService): Task DAO service
    """
    
    def __init__(self, project_service: ProjectService, task_service: TaskService):
        self.__project_service = project_service
        self.__task_service = task_service
    
    async def create_new_project(self, project_create: ProjectCreate, user_data: User) -> ResponseSchema:
        """
        Create new Project

        Args:
            project_create (ProjectCreate): Project data Validation
            user_data (User): User data (SQLAlchemy model)

        Raises:
            ConflictError: status - 409, Project name is already taken
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True} 
        """
        try:
            # Validation Project data
            project_create_dict = project_create.model_dump() # Converting Pydantic model to dict
            if await ValidationManager.validate_shemas_data_project(project_create_dict):
                # Check if Project name is taken
                for project in user_data.projects:
                    project_dict = ProjectRead.model_validate(project).model_dump()
                    if project_dict['name'] == project_create.name:
                        msg = 'Project name is already taken'
                        extra = {'project_name': project_create.name}
                        logger.warning(msg=msg, extra=extra) # log
                        raise ConflictError(msg='Project name is already taken')
                
                # Create new Project
                await self.__project_service.create_project(project_create, user_data.id)
                
                logger.info(msg=f"Project {project_create.name} was created") # log
                return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
            else:
                msg = 'Use only alphabet letters and numbers'
                logger.warning(msg=msg) # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
            
    async def get_some_project_by_name(self, project_name: str, user_data: User) -> ProjectRead:
        """
        Show another User Project

        Args:
            project_name (str): Project name
            user_data (User): User data (SQLAlchemy model)

        Raises:
            ExistError: status - 404, Project doesn't exist
            AccessError: status - 405, Don't have enough access rights to see the project
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            ProjectRead: Project data
        """
        try:
            # Validation path param
            if await ValidationManager.validate_path_data(project_name):
                # Searching for a Project in the Database
                project = await self.__project_service.get_project_by_name(project_name)
                if project is None:
                    msg = "Project doesn't exist"
                    logger.warning(msg=msg) # log
                    raise ExistError(msg="Project doesn't exist")
                
                # TODO access to other users
                # Check if User own the project
                if project.owner_id != user_data.id:
                    msg = "You don't have enough access rights to see this project"
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra) # log
                    raise AccessError(msg="You don't have enough access rights to see this project")
                
                # Show Project data
                project_model = ProjectRead.model_validate(project) # Converting SQLAlchemy model to Pydantic model (ProjectRead)
                date = re.search(r'\d{4}-\d{2}-\d{2}', f'{project_model.created_at}') # Date type YYYY-MM-DD
                project_model.created_at = date[0]
                return project_model
            else:
                msg = 'Use only alphabet letters and numbers'
                logger.warning(msg=msg) # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
    
    async def delete_current_project(self, project_name: str, user_data: User) -> ResponseSchema:
        """
        Delete Project

        Args:
            project_name (str): Project name
            user_data (User): User data (SQLAlchemy model)

        Raises:
            ExistError: status - 404, Project doesn't exist
            AccessError: status - 405, Don't have enough access rights to see the project
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True}
        """
        try:
            # Validation path params
            if await ValidationManager.validate_path_data(project_name):
                # Searching for a Project in the Database
                project = await self.__project_service.get_project_by_name(project_name)
                if project is None:
                    msg = "Project doesn't exist"
                    logger.warning(msg=msg) # log
                    raise ExistError(msg="Project doesn't exist")
                
                # Check if User own the project
                if project.owner_id != user_data.id:
                    msg = "You don't have enough access rights to see this project"
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra) # log
                    raise AccessError(msg="You don't have enough access rights to see this project")
                
                # Delete project from the Database
                await self.__project_service.delete_one_project_by_name(project_name)
                
                logger.info(msg=f"Project {project_name} has been deleted") # log
                return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
            else:
                msg = 'Use only alphabet letters and numbers'
                logger.warning(msg=msg) # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()
    
    async def create_task_in_current_project(self, project_name: str, task_create: TaskCreate, user_data: User) -> ResponseSchema:
        """
        Create Task in Project

        Args:
            project_name (str): Project name
            task_create (TaskCreate): Task data Validation
            user_data (User): User data (SQLAlcehmy model)

        Raises:
            ExistError: status - 404, Project doesn't exist
            AccessError: status - 405, Don't have enough access rights to see the project
            ValidationError: status - 400, User input symbols are incorrect
            ServerError: status - 500, SERVER ERROR

        Returns:
            ResponseSchema: {'status_code': 200, 'message': True}
        """
        try:
            # Validation path params and Task data
            if await ValidationManager.validate_path_data(project_name) and await ValidationManager.validate_schemas_data_task(task_create.model_dump()):
                # Searching for a Project in the Database
                project = await self.__project_service.get_project_by_name(project_name)
                if project is None:
                    msg = "Project doesn't exist"
                    logger.warning(msg=msg) # log
                    raise ExistError(msg="Project doesn't exist")
                
                # Check if User own the project
                if project.owner_id != user_data.id: # If User doesn't own the project
                    msg = "You don't have enough access rights to see this project"
                    extra = {'project_owner_id': project.owner_id, 'user_data_id': user_data.id}
                    logger.warning(msg=msg, extra=extra) # log
                    raise AccessError(msg="You don't have enough access rights to see this project")
                
                # Create new Task
                await self.__task_service.create_task(task_create, project.id, user_data.id)
                
                return ResponseSchema(status_code=status.HTTP_200_OK, message=True)
            else:
                msg = 'Use only alphabet letters and numbers'
                logger.warning(msg=msg) # log
                raise ValidationError(msg='Use only alphabet letters and numbers')
        except SQLAlchemyError:
            raise ServerError()

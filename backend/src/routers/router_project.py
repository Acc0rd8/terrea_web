from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.user_manager_dependency import UserManagerDependency
from src.dependencies import get_project_config_dependency
from src.models import User
from src.schemas import ProjectCreateSchema, ProjectReadSchema
from src.schemas import TaskCreateSchema
from src.schemas.response_schema import ResponseSchema
from src.services.project_config import ProjectConfig
from src.redis_config import app_redis


router_project = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router_project.post(
    '/create_project',
    name="Create new Project",
    response_model=ResponseSchema
)
async def create_project_app(
    project_create: ProjectCreateSchema,
    user_data: Annotated[User, Depends(UserManagerDependency.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config_dependency)]
):
    """
    Create new Project

    Args:
        project_create (ProjectCreateSchema): Project data Validation
        user_data (User): User data (SQLAlchemy model)

    Returns:
        ResponseSchema: {'status_code': 200, 'message': True} 
    """
    return await project_config.create_new_project(project_create, user_data)


@router_project.get(
    '/{project_name}',
    name="Get Project by name",
    response_model=ProjectReadSchema
)
@app_redis.cache
async def get_some_project(
    project_name: str,
    user_data: Annotated[User, Depends(UserManagerDependency.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config_dependency)]
):
    """
    Show another User Project

    Args:
        project_name (str): Project name
        user_data (User): User data (SQLAlchemy model)

    Returns:
        ProjectReadSchema: Project data
    """
    return await project_config.get_some_project_by_name(project_name, user_data)


@router_project.delete(
    '/{project_name}/delete',
    name="Delete Project by name",
    response_model=ResponseSchema
)
async def delete_project(
    project_name: str,
    user_data: Annotated[User, Depends(UserManagerDependency.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config_dependency)]
):
    """
    Delete Project

    Args:
        project_name (str): Project name
        user_data (User): User data (SQLAlchemy model)

    Returns:
        ResponseSchema: {'status_code': 200, 'message': True}
        """
    return await project_config.delete_current_project(project_name, user_data)


@router_project.post(
    '/{project_name}/task/create',
    name="Create new Task in Project by Project name",
    response_model=ResponseSchema
)
async def create_task_in_project(
    project_name: str,
    task_create: TaskCreateSchema,
    user_data: Annotated[User, Depends(UserManagerDependency.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config_dependency)]
):
    """
    Create Task in Project

    Args:
        project_name (str): Project name
        task_create (TaskCreateSchema): Task data Validation
        user_data (User): User data (SQLAlcehmy model)

    Returns:
        ResponseSchema: {'status_code': 200, 'message': True}
    """
    return await project_config.create_task_in_current_project(project_name, task_create, user_data)

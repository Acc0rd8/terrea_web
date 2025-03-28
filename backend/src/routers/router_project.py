from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.user_manager import UserManager
from src.dependencies.router_service import get_project_config
from src.models.model_user import User
from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.schemas.task_schemas import TaskCreate
from src.schemas.response_schema import ResponseSchema
from src.services.project_config import ProjectConfig
from src.redis_config import app_redis


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project', response_model=ResponseSchema)
async def create_project_app(
    project_create: ProjectCreate,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config)]
):
    """
    Create new Project

    Args:
        project_create (ProjectCreate): Project data Validation
        user_data (User): User data (SQLAlchemy model)

    Returns:
        ResponseSchema: {'status_code': 200, 'message': True} 
    """
    return await project_config.create_new_project(project_create, user_data)


@router.get('/{project_name}', response_model=ProjectRead)
@app_redis.cache
async def get_some_project(
    project_name: str,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config)]
):
    """
    Show another User Project

    Args:
        project_name (str): Project name
        user_data (User): User data (SQLAlchemy model)

    Returns:
        ProjectRead: Project data
    """
    return await project_config.get_some_project_by_name(project_name, user_data)


@router.delete('/{project_name}/delete', response_model=ResponseSchema)
async def delete_project(
    project_name: str,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config)]
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


@router.post('/{project_name}/task/create', response_model=ResponseSchema)
async def create_task_in_project(
    project_name: str,
    task_create: TaskCreate,
    user_data: Annotated[User, Depends(UserManager.get_current_user)],
    project_config: Annotated[ProjectConfig, Depends(get_project_config)]
):
    """
    Create Task in Project

    Args:
        project_name (str): Project name
        task_create (TaskCreate): Task data Validation
        user_data (User): User data (SQLAlcehmy model)

    Returns:
        ResponseSchema: {'status_code': 200, 'message': True}
    """
    return await project_config.create_task_in_current_project(project_name, task_create, user_data)

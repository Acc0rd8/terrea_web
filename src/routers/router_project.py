from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.dependencies.model_service import project_service, task_service
from src.dependencies.user_manager import UserManager
from src.models.model_project import Project
from src.models.model_user import User
from src.repositories.project_service import ProjectService
from src.repositories.task_service import TaskService
from src.schemas.project_schemas import ProjectCreate, ProjectRead
from src.schemas.task_schemas import TaskCreate, TaskRead
from src.services.project_config import ProjectConfig

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    return await ProjectConfig.create_new_project(project_create, user_data, project_service)


@router.get('/{project_name}')
@cache(expire=600)
async def get_some_project(project_name: str, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> ProjectRead:
    return await ProjectConfig.get_some_project_by_name(project_name, user_data, project_service)


@router.delete('/{project_name}/delete')
async def delete_project(project_name: str, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    return await ProjectConfig.delete_current_project(project_name, user_data, project_service)


@router.post('/{project_name}/task/create')
async def create_task_in_project(project_name: str, task_create: TaskCreate, user_data: Annotated[User, Depends(UserManager.get_current_user)], task_service: Annotated[TaskService, Depends(task_service)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    return await ProjectConfig.create_task_in_current_project(project_name, task_create, user_data, task_service, project_service)

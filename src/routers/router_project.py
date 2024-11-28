from fastapi import APIRouter, Depends
from typing import Annotated

from src.dependencies import project_service, task_service
from src.schemas.task_schemas import TaskRead, TaskCreate
from src.services.project_service import ProjectService
from src.business.project_config import ProjectConfig
from src.schemas.project_schemas import ProjectCreate
from src.schemas.project_schemas import ProjectRead
from src.services.task_service import TaskService
from src.business.managers import UserManager
from src.models.model_project import Project
from src.models.model_user import User


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    result = await ProjectConfig.create_new_project(project_create, user_data, project_service)
    return result


@router.get('/{project_name}')
async def get_some_project(project_name: str, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> ProjectRead:
    result = await ProjectConfig.get_some_project_by_name(project_name, user_data, project_service)
    return result


#TODO
@router.delete('/{project_name}/delete')
async def delete_project(project_name: str, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    result = await ProjectConfig.delete_current_project(project_name, user_data, project_service)
    return result


@router.post('/{project_name}/task/create')
async def create_task_in_project(project_name: str, task_create: TaskCreate, user_data: Annotated[User, Depends(UserManager.get_current_user)], task_service: Annotated[TaskService, Depends(task_service)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    result = await ProjectConfig.create_task_in_current_project(project_name, task_create, user_data, task_service, project_service)
    return result
    
from fastapi import APIRouter, Depends
from typing import Annotated

from src.services.project_service import ProjectService
from src.schemas.project_schemas import ProjectCreate
from src.schemas.project_schemas import ProjectRead
from src.business.auth_manager import UserManager
from src.business.project_config import Project
from src.schemas.task_schemas import TaskRead
from src.dependencies import project_service
from src.models.model_user import User


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    result = await Project.create_new_project(project_create, user_data, project_service)
    return result


@router.get('/{project_name}')
async def get_some_project(project_name: str, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]) -> ProjectRead:
    result = await Project.get_some_project_by_name(project_name, user_data, project_service)
    return result


#TODO
@router.delete('/{project_name}/delete', include_in_schema=False)
async def delete_project(project_name: str, user_data: Annotated[User, Depends(UserManager.get_current_user)], project_service: Annotated[ProjectService, Depends(project_service)]):
    pass
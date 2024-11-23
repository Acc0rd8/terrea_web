from fastapi import APIRouter, Depends
from typing import Annotated

from src.services.project_service import ProjectService
from src.schemas.project_schemas import ProjectCreate
from src.schemas.task_schemas import TaskRead
from src.utils.endpoint_config import Project
from src.dependencies import project_service


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    result = await Project.create_new_project(project_create, project_service)
    return result


@router.get('/{project_id}')
async def get_some_project(project_id: int, project_service: Annotated[ProjectService, Depends(project_service)]):
    result = await Project.get_some_project_by_id(project_id, project_service)
    return result
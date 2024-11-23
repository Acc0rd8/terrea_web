from fastapi import APIRouter, Depends
from typing import Annotated

from src.services.project_service import ProjectService
from src.schemas.project_schemas import ProjectCreate
from src.utils.endpoint_config import Project
from src.dependencies import project_service


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, project_service: Annotated[ProjectService, Depends(project_service)]) -> dict:
    result = Project.create_new_project(project_create, project_service)
    return result
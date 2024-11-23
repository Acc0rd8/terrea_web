from fastapi import APIRouter, Depends
from typing import Annotated

from src.services.project_service import ProjectService
from src.schemas.project_schemas import ProjectCreate
from src.dependencies import project_service


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, project_service: Annotated[ProjectService, Depends(project_service)]):
    await project_service.create_project(project_create)
    return {'message': 'Проект успешно создан'}
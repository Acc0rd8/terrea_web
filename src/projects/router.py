from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.projects.schemas import ProjectCreate
from src.database import get_async_session
from src.projects.crud.crud_projects import create_project


router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.post('/create_project')
async def create_project_app(project_create: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    await create_project(project_create, session)
    return {'message': 'Проект успешно создан'}
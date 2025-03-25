from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.repositories.project_service import ProjectService
from src.repositories.role_service import RoleService
from src.repositories.task_service import TaskService
from src.repositories.user_service import UserService
from src.utils.projects_repo import ProjectRepository
from src.utils.role_repo import RoleRepository
from src.utils.task_repo import TaskRepository
from src.utils.user_repo import UserRepository


def project_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return ProjectService(ProjectRepository(session))

def role_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return RoleService(RoleRepository(session))

def task_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return TaskService(TaskRepository(session))

def user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(UserRepository(session))
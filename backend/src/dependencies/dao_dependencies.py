from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.repositories import ProjectDAO
from src.repositories import RoleDAO
from src.repositories import TaskDAO
from src.repositories import UserDAO
from src.utils.projects_repo import ProjectRepository
from src.utils.role_repo import RoleRepository
from src.utils.task_repo import TaskRepository
from src.utils.user_repo import UserRepository


def project_dao_dependency(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return ProjectDAO(ProjectRepository(session))


def role_dao_dependency(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return RoleDAO(RoleRepository(session))


def task_dao_dependency(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return TaskDAO(TaskRepository(session))


def user_dao_dependency(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserDAO(UserRepository(session))

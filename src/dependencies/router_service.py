from fastapi import Depends
from typing import Annotated

from src.dependencies.model_service import user_service, project_service, task_service
from src.services.profile_config import ProfileConfig
from src.services.project_config import ProjectConfig
from src.repositories.user_service import UserService
from src.repositories.project_service import ProjectService
from src.repositories.task_service import TaskService


def get_profile_config(user_service: Annotated[UserService, Depends(user_service)]) -> ProfileConfig:
    return ProfileConfig(user_service=user_service)


def get_project_config(project_service: Annotated[ProjectService, Depends(project_service)], task_service: Annotated[TaskService, Depends(task_service)]) -> ProjectConfig:
    return ProjectConfig(project_service=project_service, task_service=task_service) 
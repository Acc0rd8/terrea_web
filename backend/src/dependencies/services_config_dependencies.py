from fastapi import Depends
from typing import Annotated

from src.dependencies import user_dao_dependency, project_dao_dependency, task_dao_dependency
from src.services.profile_config import ProfileConfig
from src.services.project_config import ProjectConfig
from src.repositories import UserDAO
from src.repositories import ProjectDAO
from src.repositories import TaskDAO


def get_profile_config_dependency(
    user_dao: Annotated[UserDAO, Depends(user_dao_dependency)]
) -> ProfileConfig:
    return ProfileConfig(user_dao=user_dao)


def get_project_config_dependency(
    project_dao: Annotated[ProjectDAO, Depends(project_dao_dependency)],
    task_dao: Annotated[TaskDAO, Depends(task_dao_dependency)]
) -> ProjectConfig:
    return ProjectConfig(project_dao=project_dao, task_dao=task_dao)

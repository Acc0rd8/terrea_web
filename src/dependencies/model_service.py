from src.repositories.project_service import ProjectService
from src.repositories.role_service import RoleService
from src.repositories.task_service import TaskService
from src.repositories.user_service import UserService

from src.utils.projects_repo import ProjectRepository
from src.utils.role_repo import RoleRepository
from src.utils.task_repo import TaskRepository
from src.utils.users_repo import UserRepository


def project_service():
    return ProjectService(ProjectRepository)

def role_service():
    return RoleService(RoleRepository)

def task_service():
    return TaskService(TaskRepository)

def user_service():
    return UserService(UserRepository)
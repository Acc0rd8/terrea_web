from src.repositories.project_service import ProjectService
from src.repositories.role_service import RoleService
from src.repositories.task_service import TaskService
from src.repositories.user_service import UserService

from utils.projects_repo import ProjectRepository
from utils.role_repo import RoleRepository
from utils.task_repo import TaskRepository
from utils.users_repo import UserRepository


def project_service():
    return ProjectService(ProjectRepository)

def role_service():
    return RoleService(RoleRepository)

def task_service():
    return TaskService(TaskRepository)

def user_service():
    return UserService(UserRepository)
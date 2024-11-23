from src.services.project_service import ProjectService
from src.services.role_service import RoleService
from src.services.task_service import TaskService
from src.services.user_service import UserService

from src.repositories.projects import ProjectRepository
from src.repositories.roles import RoleRepository
from src.repositories.tasks import TaskRepository
from src.repositories.users import UserRepository


def project_service():
    return ProjectService(ProjectRepository)

def role_service():
    return RoleService(RoleRepository)

def task_service():
    return TaskService(TaskRepository)

def user_service():
    return UserService(UserRepository)
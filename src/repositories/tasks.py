from src.utils.repository import SQLAlchemyRepository
from src.models.model_task import Task


class TaskRepository(SQLAlchemyRepository):
    model = Task

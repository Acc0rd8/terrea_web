from src.models import Task
from src.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task

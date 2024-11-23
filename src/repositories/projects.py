from src.utils.repository import SQLAlchemyRepository
from src.models.model_project import Project


class ProjectRepository(SQLAlchemyRepository):
    model = Project
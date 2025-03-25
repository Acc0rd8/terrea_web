from src.models.model_project import Project
from src.utils.repository import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository):
    model = Project
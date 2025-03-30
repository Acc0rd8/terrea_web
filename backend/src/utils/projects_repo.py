from src.models import Project
from src.utils.repository import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository):
    model = Project
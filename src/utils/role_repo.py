from src.utils.repository import SQLAlchemyRepository
from src.models.model_role import Role


class RoleRepository(SQLAlchemyRepository):
    model = Role

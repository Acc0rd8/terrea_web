from src.models import Role
from src.utils.repository import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository):
    model = Role

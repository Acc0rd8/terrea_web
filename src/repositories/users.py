from src.utils.repository import SQLAlchemyRepository
from src.models.model_user import User


class UserRepository(SQLAlchemyRepository):
    model = User
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import delete
import pytest

from src.schemas.user_schemas import UserUpdate 
from src.schemas.role_schemas import RoleUpdate
from src.models.model_role import Role
from src.models.model_user import User
from src.database import Base

from tests.conftest import async_engine_test, session_test


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    Base.metadata.drop_all
    Base.metadata.create_all 

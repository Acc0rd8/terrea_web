import pytest
from sqlalchemy import delete
from pydantic import BaseModel, EmailStr, Field

from src.auth.schemas import UserUpdate, RoleUpdate
from src.auth.models import Base, User, Role

from tests.conftest import engine_test, session_test


class TestUser(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=5)


class TestRole(BaseModel):
    id: int
    name: str
    permicions: list[str]
    

@pytest.fixture(scope='session', autouse=True)
def create_db():
        Base.metadata.drop_all
        Base.metadata.create_all


#TODO Add few users. Make a list of users
@pytest.fixture()
def test_user():
    user = TestUser(id=1, username='test', email='test@example.com', password='test1')
    return user


#TODO add few roles. Make a list of roles
@pytest.fixture()
def test_role():
    role = TestRole(id=1, name='user', permicions=['None'])
    return role


#TODO add few updated_users. Make a list of updated_users
@pytest.fixture()
def user_update():
    user_update = UserUpdate(username='updated', email='updated@example.com', password='updated')
    return user_update


#TODO add few updated_roles. Make a list of updated_roles
@pytest.fixture()
def role_update():
    role_update = RoleUpdate(permicions=['SomeUpdate'])
    return role_update


@pytest.fixture()
def empty_users():
    with session_test() as session:
        stmt = delete(User)
        session.execute(stmt)
        session.commit()
        
    
@pytest.fixture()
def empty_roles():
    with session_test() as session:
        stmt = delete(Role)
        session.execute(stmt)
        session.commit()
from fastapi.testclient import TestClient
from sqlalchemy import insert, delete
from httpx import AsyncClient
import asyncio
import pytest

from src.conftest import engine_test, async_session_factory_test
from src.schemas.role_schemas import RoleCreate, RoleUpdate
from src.schemas.user_schemas import UserCreate, UserUpdate
from src.repositories.role_service import RoleService
from src.repositories.user_service import UserService
from src.utils.role_repo import RoleRepository
from src.utils.user_repo import UserRepository
from src.database import Base
from src.models.model_role import Role
from src.models.model_user import User
from src.models.model_project import Project
from src.models.model_task import Task
from src.main import app as fastapi_app


@pytest.fixture(scope='function', autouse=True)
async def database_prepare():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture()
async def clear_users():
    async with async_session_factory_test() as session:
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()


#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture()
async def clear_roles():
    async with async_session_factory_test() as session:
        stmt = delete(Role)
        await session.execute(stmt)
        await session.commit()


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    
    
@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


# SERVICE FICTURES
@pytest.fixture(scope='function')
async def role_service_test():
    async with async_session_factory_test() as session:
        yield RoleService(RoleRepository(session))
        
@pytest.fixture(scope='function')
async def user_service_test():
    async with async_session_factory_test() as session:
        yield UserService(UserRepository(session))


# ROLE PYDANTIC SCHEMAS FICTURES
#TODO Add list of roles_create
@pytest.fixture(scope='function')
async def role_create():
    role_create = RoleCreate(name='test', permicions=['None'])
    return role_create

#TODO Add list of roles_update
@pytest.fixture(scope='function')
async def role_update():
    role_update = RoleUpdate(name='test_updated', permicions=['updated'])
    return role_update


# USER PYDANTIC SCHEMAS FICTURES
#TODO Add list of user_create
@pytest.fixture(scope='function')
async def user_create():
    user_create = UserCreate(email='test@example.com', username='test1', password='test1')
    return user_create

#TODO Add list of user_update
@pytest.fixture(scope='function')
async def user_update():
    user_update = UserUpdate(email='testupdated@example.com', username='test1_updated', password='updated')
    return user_update
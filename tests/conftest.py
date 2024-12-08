from fastapi.testclient import TestClient
from sqlalchemy import insert, delete
from httpx import AsyncClient
import asyncio
import pytest

from src.conftest import engine_test, async_session_factory_test
from src.database import Base
from src.models.model_role import Role
from src.models.model_user import User
from src.models.model_project import Project
from src.models.model_task import Task
from src.main import app as fastapi_app
from src.schemas.role_schemas import RoleCreate


@pytest.fixture(scope='session', autouse=True)
async def database_prepare():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session_factory_test() as session:
        stmt = insert(Role).values(id=1, name='user', permicions=[None])
        await session.execute(stmt)
        await session.commit()


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


#TODO Change session fixture to Service fixture
@pytest.fixture(scope='function')
async def session():
    async with async_session_factory_test() as session:
        yield session


#TODO Add list of roles
@pytest.fixture(scope='function')
async def role_create():
    role_create = RoleCreate(name='test', permicions=['None'])
    return role_create
import asyncio
from httpx import AsyncClient
from sqlalchemy import insert
import pytest

from tests.conftest import engine_test, async_session_factory_test
from src.main import app as fastapi_app
from src.database import Base
from src.models.model_role import Role
from src.models.model_user import User
from src.models.model_project import Project
from src.models.model_task import Task


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """ Create an instance of the default event loop for each test case. """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture(scope='session', autouse=True)
async def database_prepare():
    """Create database session with starting api tests"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # DELETE all tables
        await conn.run_sync(Base.metadata.create_all) # CREATE empty tables
        
    async with async_session_factory_test() as session:
        stmt = insert(Role).values(id=1, name='test', permicions=['None'])
        await session.execute(stmt)
        await session.commit()
        

# ASYNC CLIENT FICTURES
@pytest.fixture(scope='function')
async def ac():
    """ Creates async client

    Yields:
        AsyncClient: User
    """
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac
        
        
@pytest.fixture(scope='class')
async def authenticated_ac():
    """ Authenticated async Client

    Yields:
        AsyncClient: User
    """
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        response = await ac.post('/profile/login', json={  # HTTP POST
            'email': 'test1@example.com',
            'username': 'test1',
            'password': 'test1',
        })
        
        assert response.status_code == 200
        assert response.cookies.get('user_access_token')
        assert response.cookies['user_access_token']
        
        yield ac
        

@pytest.fixture(scope='class', autouse=False)
async def create_ac_for_project():
    """ Authenticated async Client for Project tests """
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        await ac.post('/profile/register', json={  # HTTP POST
            'email': 'test1@example.com',
            'username': 'test1',
            'password': 'test1',
        })
        

@pytest.fixture(scope='function', autouse=False)
async def create_project(authenticated_ac: AsyncClient):
    """ Create new Project

    Args:
        authenticated_ac (AsyncClient): Authenticated User
    """
    await authenticated_ac.post('/projects/create_project', json={  # HTTP POST
        'name': 'project1'
    })
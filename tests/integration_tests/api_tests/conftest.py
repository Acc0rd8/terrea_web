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
async def database_prepare():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session_factory_test() as session:
        stmt = insert(Role).values(id=1, name='test', permicions=['None'])
        await session.execute(stmt)
        await session.commit()
        

# ASYNC CLIENT FICTURES
@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac
        
@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        await ac.post('/profile/register', json={
            'email': 'test@example.com',
            'username': 'test1',
            'password': 'test',
        })
        assert ac.cookies['user_access_token']
        yield ac
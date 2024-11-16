import pytest
import asyncio
from sqlalchemy import delete

from src.auth.schemas import UserCreate, UserUpdate
from src.auth.models import Base, User, Role

from tests.conftest import engine_test, async_session_test


@pytest.fixture(scope='session', autouse=True)
async def create_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture()
def user_create():
    user = UserCreate(username='test', email='test@example.com', password='test1')
    return user


@pytest.fixture()
def user_update():
    user = UserUpdate(username='updated', email='updated@example.com', password='updated')
    return user


@pytest.fixture()
async def empty_users():
    async with async_session_test() as session:
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()
        
    
@pytest.fixture()
async def empty_roles():
    async with async_session_test() as session:
        stmt = delete(Role)
        await session.execute(stmt)
        await session.commit()
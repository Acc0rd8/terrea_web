from sqlalchemy import insert, delete
import asyncio
import pytest

from tests.conftest import engine_test, async_session_factory_test
from src.database import Base
from src.schemas import ProjectCreateSchema
from src.schemas import ProjectUpdateSchema
from src.schemas import RoleCreateSchema
from src.schemas import RoleUpdateSchema
from src.schemas import UserCreateSchema
from src.schemas import UserUpdateSchema
from src.schemas import TaskCreateSchema
from src.schemas import TaskUpdateSchema
from src.repositories import UserDAO
from src.repositories import ProjectDAO
from src.repositories import TaskDAO
from src.repositories import RoleDAO
from src.utils.projects_repo import ProjectRepository
from src.utils.role_repo import RoleRepository
from src.utils.user_repo import UserRepository
from src.utils.task_repo import TaskRepository
from src.models import Role
from src.models import User
from src.models import Project
from src.models import Task


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """ Create an instance of the default event loop for each test case. """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def database_prepare():
    """ Create database session """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # DROP all tables
        await conn.run_sync(Base.metadata.create_all) # CREATE empty tables


# MOCK
#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def clear_users():
    """ Clear all Users after test """
    async with async_session_factory_test() as session:
        stmt = delete(User) # DELETE all Users
        await session.execute(stmt)
        await session.commit()

#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def clear_roles():
    """ Clear all Roles after test"""
    async with async_session_factory_test() as session:
        stmt = delete(Role) # DELETE all Roles
        await session.execute(stmt)
        await session.commit()
        
#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def clear_tasks():
    """ Clear all Tasks after test """
    async with async_session_factory_test() as session:
        stmt = delete(Task) # DELETE all Tasks
        await session.execute(stmt)
        await session.commit()
        
#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def clear_projects():
    """ Clear all Projects after test """
    async with async_session_factory_test() as session:
        stmt = delete(Project) # DELETE all Projects
        await session.execute(stmt)
        await session.commit()

#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def create_user():
    """ Create mock User """
    async with async_session_factory_test() as session:
        stmt = insert(User).values(id=1, username='test1', email='test@example.com', password='test1')
        await session.execute(stmt)
        await session.commit()

#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def create_role():
    """ Create mock Role """
    async with async_session_factory_test() as session:
        stmt = insert(Role).values(id=1, name='test', permicions=['None'])
        await session.execute(stmt)
        await session.commit()
        
#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def create_project():
    """ Create mock Project """
    async with async_session_factory_test() as session:
        stmt = insert(Project).values(id=1, name='test', owner_id=1)
        await session.execute(stmt)
        await session.commit()
        
#TODO change using async_session_factory_test to async_session_generator(get_async_session_test)
@pytest.fixture(scope='function')
async def create_task():
    """ Create mock task """
    async with async_session_factory_test() as session:
        stmt = insert(Task).values(id=1, customer_id=1, performer_id=1, project_id=1, name='test', deadline=None)
        await session.execute(stmt)
        await session.commit()


# SERVICE FICTURES
@pytest.fixture(scope='function')
async def role_service_test():
    async with async_session_factory_test() as session:
        yield RoleDAO(RoleRepository(session))
        
@pytest.fixture(scope='function')
async def user_service_test():
    async with async_session_factory_test() as session:
        yield UserDAO(UserRepository(session))
        
@pytest.fixture(scope='function')
async def project_service_test():
    async with async_session_factory_test() as session:
        yield ProjectDAO(ProjectRepository(session))
        
@pytest.fixture(scope='function')
async def task_service_test():
    async with async_session_factory_test() as session:
        yield TaskDAO(TaskRepository(session))


# ROLE PYDANTIC SCHEMAS FICTURES
#TODO Add list of roles_create
@pytest.fixture(scope='function')
async def role_create():
    """ Mock RoleCreate schema

    Returns:
        RoleCreate: ...
    """
    role_create = RoleCreateSchema(name='test', permicions=['None'])
    return role_create

#TODO Add list of roles_update
@pytest.fixture(scope='function')
async def role_update():
    """ Mock RoleUpdate schema

    Returns:
        RoleUpdate: ...
    """
    role_update = RoleUpdateSchema(name='test_updated', permicions=['updated'])
    return role_update


# USER PYDANTIC SCHEMAS FICTURES
#TODO Add list of user_create
@pytest.fixture(scope='function')
async def user_create():
    """ Mock UserCreate schema

    Returns:
        UserCreate: ...
    """
    user_create = UserCreateSchema(email='test@example.com', username='test1', password='test1')
    return user_create

#TODO Add list of user_update
@pytest.fixture(scope='function')
async def user_update():
    """ Mcok UserUpdate schema

    Returns:
        UserUpdate: ...
    """
    user_update = UserUpdateSchema(email='testupdated@example.com', username='test1_updated', password='updated')
    return user_update


# PROJECT PYDANTIC SCHEMAS FICTURES
#TODO Add list of project_create
@pytest.fixture(scope='function')
async def project_create():
    """ Mock ProjectCreate schema

    Returns:
        ProjectCreate: ...
    """
    project_create = ProjectCreateSchema(name='test')
    return project_create

#TODO Add list of project_update
@pytest.fixture(scope='function')
async def project_update():
    """ Mock ProjectUpdate schema

    Returns:
        ProjectUpdate: ...
    """
    project_update = ProjectUpdateSchema(name='test_updated')
    return project_update


# TASK PYDANTIC SCHEMAS FICTURES
#TODO Add list of task_create
@pytest.fixture(scope='function')
async def task_create():
    """ Mock TaskCreate schema

    Returns:
        TaskCreate: ...
    """
    task_create = TaskCreateSchema(customer_id=1, performer_id=1, name='test', deadline=None)
    return task_create

#TODO Add list of task_update
@pytest.fixture(scope='function')
async def task_update():
    """ Mock TaskUpdate schema

    Returns:
        TaskUpdate: ...
    """
    task_update = TaskUpdateSchema(name='test_updated', deadline=None)
    return task_update

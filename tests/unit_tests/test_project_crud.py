# TEST Project CRUD requests - TST2 

import pytest

from src.schemas.project_schemas import ProjectCreate, ProjectUpdate
from src.schemas.task_schemas import TaskCreate, TaskUpdate
from src.repositories.project_service import ProjectService
from src.repositories.task_service import TaskService


class TestProjectCRUD:
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_id, response', [
        (1, {'message': 'Project has been created'})
    ])
    async def test_create_project(self, user_id: int, response: dict, project_create: ProjectCreate, project_service_test: ProjectService):
        """ Test creating Project

        Args:
            user_id (int): user id in the Database
            response (dict): test response
            project_create (ProjectCreate): Project create Validation
            project_service_test (ProjectService): Project DAO service
        """
        result = await project_service_test.create_project(project_create, user_id)
        assert result == response


    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test>'),
        (2, 'None')
    ])
    async def test_get_project_by_id(self, project_id: int, response: str, project_service_test: ProjectService):
        """ Test reading Project by id from the Database

        Args:
            project_id (int): Project id in the Database
            response (str): test response
            project_service_test (ProjectService): Project DAO service
        """
        result = await project_service_test.get_project_by_id(project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', f'<Project: id = 1, name = test>'),
        ('None', 'None')
    ])
    async def test_get_project_by_name(self, project_name: str, response: str, project_service_test: ProjectService):
        """ Test reading Project by name from the Database

        Args:
            project_name (str): Project name in the Database
            response (str): test response
            project_service_test (ProjectService): Project DAO service
        """        
        result = await project_service_test.get_project_by_name(project_name)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test_updated>'),
        (2, 'None')
    ])
    async def test_update_project(self, project_id: int, response: str, project_update: ProjectUpdate, project_service_test: ProjectService):
        """ Test updating Project

        Args:
            project_id (int): Project id in the Database
            response (str): test response
            project_update (ProjectUpdate): Project update Validation
            project_service_test (ProjectService): Project DAO service
        """
        result = await project_service_test.update_project(project_update, project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_id(self, project_id: int, response: dict, project_service_test: ProjectService):
        """ Test deleting one Project by id

        Args:
            project_id (int): Project id in the Database
            response (dict): test response
            project_service_test (ProjectService): Project DAO service
        """
        result = await project_service_test.delete_one_project_by_id(project_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_name(self, project_name: str, response: dict, project_service_test: ProjectService):
        """ Test deleting one Project by name

        Args:
            project_name (str): Project name in the Database
            response (dict): test response
            project_service_test (ProjectService): Project DAO service
        """
        result = await project_service_test.delete_one_project_by_name(project_name)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    async def test_delete_all_projects(self, project_service_test: ProjectService):
        """ Test deleting all Projects

        Args:
            project_service_test (ProjectService): Project DAO service
        """
        result = await project_service_test.delete_all_projects()
        assert result == {'message': 'All Projects have been deleted'}


class TestTaskCRUD:
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, customer_id, response', [
        (1, 1, {'message': 'Task has been created'})
    ])
    async def test_create_task(self, project_id: int, customer_id: int, response: dict, task_create: TaskCreate, task_service_test: TaskService):
        """ Test creating Task

        Args:
            project_id (int): Project id in the Database
            customer_id (int): User id in the Database
            response (dict): test response
            task_create (TaskCreate): Task create Validation
            task_service_test (TaskService): Task DAO service
        """
        result = await task_service_test.create_task(task_create, project_id, customer_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, '<Task: id = 1, name = test, project_id = 1>'),
        (2, 'None')
    ])
    async def test_get_task(self, task_id: int, response: str, task_service_test: TaskService):
        """ Test reading Task from the Database

        Args:
            task_id (int): Task id in the Database
            response (str): test response
            task_service_test (TaskService): Task DAO service
        """
        result = await task_service_test.get_task(task_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, '<Task: id = 1, name = test_updated, project_id = 1>'),
        (2, 'None')
    ])
    async def test_update_task(self, task_id: int, response: str, task_update: TaskUpdate, task_service_test: TaskService):
        """ Test updating Task

        Args:
            task_id (int): Task id in the Database
            response (str): test response
            task_update (TaskUpdate): Task update Validation
            task_service_test (TaskService): Task DAO service
        """
        result = await task_service_test.update_task(task_update, task_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, {'message': 'Task has been deleted'})
    ])
    async def test_delete_one_task(self, task_id: int, response: dict, task_service_test: TaskService):
        """ Test deleting one Task

        Args:
            task_id (int): Task id in the Database
            response (dict): test response
            task_service_test (TaskService): Task DAO service
        """
        result = await task_service_test.delete_one_task(task_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    async def test_delete_all_tasks(self, task_service_test: TaskService):
        """ Test deleting all Tasks

        Args:
            task_service_test (TaskService): Task DAO service
        """
        result = await task_service_test.delete_all_tasks()
        assert result == {'message': 'All Tasks have been deleted'}
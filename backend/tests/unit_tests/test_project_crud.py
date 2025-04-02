# TEST Project CRUD requests - TSTU2 

import pytest

from src.schemas import TaskCreateSchema
from src.schemas import TaskUpdateSchema
from src.schemas import ProjectCreateSchema
from src.schemas import ProjectUpdateSchema
from src.repositories import ProjectDAO
from src.repositories import TaskDAO


class TestProjectCRUD:
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_id, response', [
        (1, {'message': 'Project has been created'})
    ])
    async def test_create_project(self, user_id: int, response: dict, project_create: ProjectCreateSchema, project_dao_test: ProjectDAO):
        """ Test creating Project

        Args:
            user_id (int): user id in the Database
            response (dict): test response
            project_create (ProjectCreateSchema): Project create Validation
            project_dao_test (ProjectDAO): Project DAO service
        """
        result = await project_dao_test.create_project(project_create, user_id)
        assert result == response


    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test>'),
        (2, 'None')
    ])
    async def test_get_project_by_id(self, project_id: int, response: str, project_dao_test: ProjectDAO):
        """ Test reading Project by id from the Database

        Args:
            project_id (int): Project id in the Database
            response (str): test response
            project_dao_test (ProjectDAO): Project DAO service
        """
        result = await project_dao_test.get_project_by_id(project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', f'<Project: id = 1, name = test>'),
        ('None', 'None')
    ])
    async def test_get_project_by_name(self, project_name: str, response: str, project_dao_test: ProjectDAO):
        """ Test reading Project by name from the Database

        Args:
            project_name (str): Project name in the Database
            response (str): test response
            project_dao_test (ProjectDAO): Project DAO service
        """        
        result = await project_dao_test.get_project_by_name(project_name)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test_updated>'),
        (2, 'None')
    ])
    async def test_update_project(self, project_id: int, response: str, project_update: ProjectUpdateSchema, project_dao_test: ProjectDAO):
        """ Test updating Project

        Args:
            project_id (int): Project id in the Database
            response (str): test response
            project_update (ProjectUpdateSchema): Project update Validation
            project_dao_test (ProjectDAO): Project DAO service
        """
        result = await project_dao_test.update_project(project_update, project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_id(self, project_id: int, response: dict, project_dao_test: ProjectDAO):
        """ Test deleting one Project by id

        Args:
            project_id (int): Project id in the Database
            response (dict): test response
            project_dao_test (ProjectDAO): Project DAO service
        """
        result = await project_dao_test.delete_one_project_by_id(project_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_name(self, project_name: str, response: dict, project_dao_test: ProjectDAO):
        """ Test deleting one Project by name

        Args:
            project_name (str): Project name in the Database
            response (dict): test response
            project_dao_test (ProjectDAO): Project DAO service
        """
        result = await project_dao_test.delete_one_project_by_name(project_name)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    async def test_delete_all_projects(self, project_dao_test: ProjectDAO):
        """ Test deleting all Projects

        Args:
            project_dao_test (ProjectDAO): Project DAO service
        """
        result = await project_dao_test.delete_all_projects()
        assert result == {'message': 'All Projects have been deleted'}


class TestTaskCRUD:
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, customer_id, response', [
        (1, 1, {'message': 'Task has been created'})
    ])
    async def test_create_task(self, project_id: int, customer_id: int, response: dict, task_create: TaskCreateSchema, task_dao_test: TaskDAO):
        """ Test creating Task

        Args:
            project_id (int): Project id in the Database
            customer_id (int): User id in the Database
            response (dict): test response
            task_create (TaskCreateSchema): Task create Validation
            task_dao_test (TaskDAO): Task DAO service
        """
        result = await task_dao_test.create_task(task_create, project_id, customer_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, '<Task: id = 1, name = test, project_id = 1>'),
        (2, 'None')
    ])
    async def test_get_task(self, task_id: int, response: str, task_dao_test: TaskDAO):
        """ Test reading Task from the Database

        Args:
            task_id (int): Task id in the Database
            response (str): test response
            task_dao_test (TaskDAO): Task DAO service
        """
        result = await task_dao_test.get_task(task_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, '<Task: id = 1, name = test_updated, project_id = 1>'),
        (2, 'None')
    ])
    async def test_update_task(self, task_id: int, response: str, task_update: TaskUpdateSchema, task_dao_test: TaskDAO):
        """ Test updating Task

        Args:
            task_id (int): Task id in the Database
            response (str): test response
            task_update (TaskUpdateSchema): Task update Validation
            task_dao_test (TaskDAO): Task DAO service
        """
        result = await task_dao_test.update_task(task_update, task_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, {'message': 'Task has been deleted'})
    ])
    async def test_delete_one_task(self, task_id: int, response: dict, task_dao_test: TaskDAO):
        """ Test deleting one Task

        Args:
            task_id (int): Task id in the Database
            response (dict): test response
            task_dao_test (TaskDAO): Task DAO service
        """
        result = await task_dao_test.delete_one_task(task_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    async def test_delete_all_tasks(self, task_dao_test: TaskDAO):
        """ Test deleting all Tasks

        Args:
            task_dao_test (TaskDAO): Task DAO service
        """
        result = await task_dao_test.delete_all_tasks()
        assert result == {'message': 'All Tasks have been deleted'}

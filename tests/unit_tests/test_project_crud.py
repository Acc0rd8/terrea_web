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
        result = await project_service_test.create_project(project_create, user_id)
        assert result == response


    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test>'),
        (2, 'None')
    ])
    async def test_get_project_by_id(self, project_id: int, response: str, project_service_test: ProjectService):
        result = await project_service_test.get_project_by_id(project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', f'<Project: id = 1, name = test>'),
        ('None', 'None')
    ])
    async def test_get_project_by_name(self, project_name: str, response: str, project_service_test: ProjectService):
        result = await project_service_test.get_project_by_name(project_name)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test_updated>'),
        (2, 'None')
    ])
    async def test_update_project(self, project_id: int, response: str, project_update: ProjectUpdate, project_service_test: ProjectService):
        result = await project_service_test.update_project(project_update, project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_id(self, project_id: int, response: dict, project_service_test: ProjectService):
        result = await project_service_test.delete_one_project_by_id(project_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_name(self, project_name: str, response: dict, project_service_test: ProjectService):
        result = await project_service_test.delete_one_project_by_name(project_name)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('response', [
        ({'message': 'All Projects have been deleted'})
    ])
    async def test_delete_all_projects(self, response: dict, project_service_test: ProjectService):
        result = await project_service_test.delete_all_projects()
        assert result == response


class TestTaskCRUD:
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, customer_id, response', [
        (1, 1, {'message': 'Task has been created'})
    ])
    async def test_create_task(self, project_id: int, customer_id: int, response: dict, task_create: TaskCreate, task_service_test: TaskService):
        result = await task_service_test.create_task(task_create, project_id, customer_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, '<Task: id = 1, name = test, project_id = 1>'),
        (2, 'None')
    ])
    async def test_get_task(self, task_id: int, response: str, task_service_test: TaskService):
        result = await task_service_test.get_task(task_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, '<Task: id = 1, name = test_updated, project_id = 1>'),
        (2, 'None')
    ])
    async def test_update_task(self, task_id: int, response: str, task_update: TaskUpdate, task_service_test: TaskService):
        result = await task_service_test.update_task(task_update, task_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('task_id, response', [
        (1, {'message': 'Task has been deleted'})
    ])
    async def test_delete_one_task(self, task_id: int, response: dict, task_service_test: TaskService):
        result = await task_service_test.delete_one_task(task_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_tasks', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project', 'create_task')
    @pytest.mark.parametrize('response', [
        ({'message': 'All Tasks have been deleted'})
    ])
    async def test_delete_all_tasks(self, response: dict, task_service_test: TaskService):
        result = await task_service_test.delete_all_tasks()
        assert result == response
import pytest

from src.schemas.project_schemas import ProjectCreate, ProjectUpdate
from src.schemas.task_schemas import TaskCreate, TaskUpdate
from src.repositories.project_service import ProjectService


#TODO
class TestProjectCRUD:
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_id', [
        (1)
    ])
    async def test_create_project(self, project_create: ProjectCreate, user_id: int, project_service_test: ProjectService):
        result = await project_service_test.create_project(project_create, user_id)
        assert result == {'message': 'Project has been created'}


    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test>')
    ])
    async def test_get_project_by_id(self, project_id: int, response: str, project_service_test: ProjectService):
        result = await project_service_test.get_project_by_id(project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', f'<Project: id = 1, name = test>')
    ])
    async def test_get_project_by_name(self, project_name: str, response: str, project_service_test: ProjectService):
        result = await project_service_test.get_project_by_name(project_name)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, f'<Project: id = 1, name = test_updated>')
    ])
    async def test_update_project(self, project_id: int, response: str, project_update: ProjectUpdate, project_service_test: ProjectService):
        result = await project_service_test.update_project(project_update, project_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_id, response', [
        (1, {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_id(self, project_id: int, response: str, project_service_test: ProjectService):
        result = await project_service_test.delete_one_project_by_id(project_id)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    @pytest.mark.parametrize('project_name, response', [
        ('test', {'message': 'Project has been deleted'})
    ])
    async def test_delete_one_project_by_name(self, project_name: str, response: str, project_service_test: ProjectService):
        result = await project_service_test.delete_one_project_by_name(project_name)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_projects', 'clear_users', 'clear_roles', 'create_role', 'create_user', 'create_project')
    async def test_delete_all_projects(self, project_service_test: ProjectService):
        result = await project_service_test.delete_all_projects()
        assert result == {'message': 'All Projects have been deleted'}

#TODO
class TestTaskCRUD:
    async def test_create_task(self):
        pass
    
    async def test_get_task(self):
        pass
    
    async def test_update_task(self):
        pass
    
    async def test_delete_one_task(self):
        pass
    
    async def test_delete_all_tasks(self):
        pass
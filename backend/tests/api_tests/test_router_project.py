# TEST project API - TSTA2

import pytest

from httpx import AsyncClient
from datetime import date


'''
!!!
Run tests only with 'TestRouterProject' CLASS or 'test_router_project.py' FILE or 'api_tests' FOLDER or 'tests' FOLDER, otherwise there will be an error
!!!
'''
class TestRouterProject:
    @pytest.mark.usefixtures('create_ac_for_project')
    @pytest.mark.parametrize('project_name, status_code', [
        ('project1', 200),  # Correct request
        ('#project2', 400)  # Invalid Project name
    ])
    async def test_create_new_project(self, authenticated_ac: AsyncClient, project_name: str, status_code: int):
        """ Test creating new Project

        Args:
            authenticated_ac (AsyncClient): Authenticated User
            project_name (str): Project name
            status_code (int): test status_code
        """
        response = await authenticated_ac.post('/projects/create_project', json={  # HTTP POST
            'name': project_name
        })
        
        response_data = response.json()
        
        assert response.status_code == status_code
        if status_code == 200:
            assert response_data == {'message': 'Project has been created', 'status_code': 200}
    
    
    @pytest.mark.parametrize('project_name, status_code', [
        ('project1', 200),  # Correct request
        ('project2', 404),  # Project not found
        ('projest%3', 404),  # Project not found
    ])    
    async def test_get_some_project_by_name(self, authenticated_ac: AsyncClient, project_name: str, status_code: int):
        """ Test reading some project

        Args:
            authenticated_ac (AsyncClient): Authenticated User
            project_name (str): Project name
            status_code (int): test status_code
        """
        response = await authenticated_ac.get(f'/projects/{project_name}')  # HTTP GET
        
        response_data = {key: value for key, value in response.json().items() if key != 'created_at' and key != 'owner_id'}
        
        assert response.status_code == status_code
        if status_code == 200:
            assert response_data == {
                'id': 1,
                'name': project_name,
                'project_tasks': []
            }
    
    
    @pytest.mark.parametrize('project_name, status_code', [
        ('project1', 200),  # Correct request
        ('project2', 404),  # Project not found
        ('project&3', 404),  # Project not found
    ])
    async def test_delete_current_project(self, authenticated_ac: AsyncClient, project_name: str, status_code: int):
        """ Test deleting project by name

        Args:
            authenticated_ac (AsyncClient): Authenticated User
            project_name (str): Project name
            status_code (int): test status_code
        """
        response = await authenticated_ac.delete(f'/projects/{project_name}/delete')  # HTTP DELETE
        
        response_data = response.json()
        
        assert response.status_code == status_code
        if status_code == 200:
            assert response_data == {'message': 'Project has been deleted', 'status_code': 200}
    
    
    @pytest.mark.usefixtures('create_project')
    @pytest.mark.parametrize('project_name, customer_id, performer_id, name, deadline, status_code', [
        ('project1', 6, 6, 'task1', '2030-04-04', 200),  # Correct request
        ('project1', 6, 6, 'task2', None, 200),  # Correct reques
        ('project1', 'str', 6, 'task3', '2030-05-04', 422),  # Invalid customer_id
        ('project2', 6, 6, 'task4', None, 404),  # Project not found
    ])
    async def test_create_task_in_current_project(self, authenticated_ac: AsyncClient, project_name: str, customer_id: int, performer_id: int, name: str, deadline: date, status_code: int):
        """ Test creating task in project

        Args:
            authenticated_ac (AsyncClient): Authenticated User
            project_name (str): Project name
            customer_id (int): Task customer id
            performer_id (int): Task performer id
            name (str): Task name
            deadline (date): Task deadline
            status_code (int): test status_code
        """
        response = await authenticated_ac.post(f'/projects/{project_name}/task/create', json={  # HTTP POST
            'customer_id': customer_id,
            'performer_id': performer_id,
            'name': name,
            'deadline': deadline,
        })
        
        response_data = response.json()
        
        assert response.status_code == status_code
        if status_code == 200:
            assert response_data == {'message': 'Task has been created', 'status_code': 200}

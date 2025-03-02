# TEST application dependencies - TST4

import pytest

from pydantic import EmailStr

from src.dependencies.security import Security

class TestSecurity:
    @pytest.mark.parametrize('id, username, email, password, response', [
        ('1', 'test1', 'test1@example.com', 'test1', True),
        ('2', 'test2%', 'test2@example.com', 'test2', False),
        ('3', 'test3', 'test3@example.com', 'test3$', False),
    ])
    async def test_validate_schemas_data_user(self, id: str, username: str, email: EmailStr, password: str, response: bool):
        """ Test validating User data schemas

        Args:
            id (int): User id
            username (str): User name
            email (EmailStr): User email
            password (str): User password
            response (bool): test response
        """
        user_data_dict = {'id': id, 'username': username, 'email': email, 'password': password}
        result = await Security.validate_schemas_data_user(user_data_dict)
        assert result == response
        
    
    @pytest.mark.parametrize('id, name, owner_id, response', [
        ('1', 'test1', '1', True),
        ('2', 'test2%', '1', False),
        ('3', ')test3', '1', False),
        ('4', '4test', '1', True)
    ])
    async def test_validate_shemas_data_project(self, id: str, name: str, owner_id: str, response: bool):
        """ Test validating Project data schemas

        Args:
            id (str): Project id
            name (str): Project name
            owner_id (str): Project owner_id
            response (bool): test response
        """
        project_data_dict = {'id': id, 'name': name, 'owner_id': owner_id}
        result = await Security.validate_shemas_data_project(project_data_dict)
        assert result == response
    
    
    @pytest.mark.parametrize('name, response', [
        ('test1', True),
        ('@test2', False),
        ('<test3', False),
        ('4test', True)
    ])
    async def test_validate_schemas_data_task(self, name: str, response: bool):
        """ Test validating Task data schemas

        Args:
            name (str): Task name
            response (bool): test response
        """
        task_data_dict = {'name': name}
        result = await Security.validate_schemas_data_task(task_data_dict)
        assert result == response
    
    
    @pytest.mark.parametrize('data, response', [
        ('test1', True),
        ('%test2', False),
        ('te/st3^', False),
        ('4test', True)
    ])
    async def test_validate_path_data(self, data: str, response: bool):
        """ Test validate data

        Args:
            data (str): some data
            response (bool): test response
        """
        result = await Security.validate_path_data(data)
        assert result == response
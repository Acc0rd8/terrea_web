# TEST profile API - TSTA1

import pytest

from httpx import AsyncClient
from pydantic import EmailStr


'''
!!!
Run tests only with TestRouterProfile CLASS or test_router_profile.py FILE or api_tests FOLDER or tests FOLDER, otherwise there will be an error
!!!
'''
class TestRouterProfile:
    @pytest.mark.parametrize('email, username, password, status_code', [
        ('test1@example.com', 'test1', 'test1', 200), # Correct registration
        ('test1@example.com', 'test2', 'test2', 409), # email is already taken
        ('test2@example.com', 'test1', 'test1', 409), # username is already taken
        ('test3', 'test3', 'test3', 422) # email is incorrect
    ])
    async def test_register_user(self, ac: AsyncClient, email: EmailStr, username: str, password: str, status_code: int):
        """ Test User registration

        Args:
            ac (AsyncClient): User
            email (EmailStr): User email
            username (str): User name
            password (str): User password
            status_code (int): test status code
        """
        response = await ac.post('/profile/register', json={  # HTTP POST
            'email': email,
            'username': username,
            'password': password
        })
        
        assert response.status_code == status_code
        if status_code == 200:  # If the User has registred
            assert response.cookies.get('user_access_token')
            assert response.cookies['user_access_token']
        
        
    @pytest.mark.parametrize('email, password, status_code', [
        ('test1@example.com', 'test1', 200), # Correct login
        ('test2@example.com', 'test2', 401), # User doesn't exist
        ('test3', 'test3', 422) # Path validation Error
    ])
    async def test_user_authentication(self, ac: AsyncClient, email: EmailStr, password: str, status_code: int):
        """ Test user Login

        Args:
            ac (AsyncClient): User
            email (EmailStr): User email
            password (str): User password
            status_code (int): test status_codeS
        """
        response = await ac.post('/profile/login', json={  # HTTP POST
            'email': email,
            'password': password
        })
        
        assert response.status_code == status_code
        if status_code == 200:  # If the User has been authorized
            assert response.cookies.get('user_access_token')
            assert response.cookies['user_access_token']
            
    
    async def test_get_user_me(self, authenticated_ac: AsyncClient):
        """ Tesk get User profile

        Args:
            authenticated_ac (AsyncClient): Authenticated User
        """
        response = await authenticated_ac.get('/profile/me')  # HTTP GET
        response_data = {key: value for key, value in response.json().items() if key != 'registred_at'}
        
        assert response.status_code == 200
        assert response_data == {
            'email': 'test1@example.com',
            'username': 'test1',
            'role_id': 1,
            'is_active': True,
            'projects': [],
            'user_tasks': [],
        }
    

    @pytest.mark.parametrize('email, old_username, old_password, new_username, new_password, status_code', [
        ('test2@example.com', 'test2', 'test2', 'test2_updated', 'test2_updated', 200),  # Correct updating
        ('test3@example.com', 'test3', 'test3', 'test3^updated', 'test3_updated', 400),  # new_username is incorrect 
        ('test4@example.com', 'test4', 'test4', 'test4_updated', 'test4*updated', 400),  # new_password is incorrect
        ('test5@example.com', 'test5', 'test5', 'test5', '123', 422)  # new_password is too short
    ])
    async def test_update_current_user(self, ac: AsyncClient, email: EmailStr, old_username: str, old_password: str, new_username: str, new_password: str, status_code: int):
        """ Test updating current User (Need to fix)

        Args:
            ac (AsyncClient): User
            new_username (str): new User username
            new_password (str): new User password
            status_code (int): test status_code
        """
        response = await ac.post('/profile/register', json={  # HTTP POST.  Creating new User
            'email': email,
            'username': old_username,
            'password': old_password,
        })
        
        response = await ac.patch('/profile/update_profile', json={  # HTTP PATCH.  Updating new User
            'email': 'test2@example.com',
            'username': new_username,
            'password': new_password,
            'is_active': True
        })
        response_data = {key: value for key, value in response.json().items() if key != 'registred_at'}
        
        assert response.status_code == status_code
        if status_code == 200:  # If the User successfully updated
            assert response_data == {
                'email': email,
                'username': new_username,
                'role_id': 1,
                'is_active': True,
                'projects': [],
                'user_tasks': [],
            }
        
    
    @pytest.mark.parametrize('username, email, status_code', [
        ('test1', 'test1@example.com', 200),  # Correct request
        ('test2_updated', 'test2@example.com', 200),  # Correct request
        ('some_name', None, 404),  # User doesn't exist
        ('user name', None, 400)  # Invalid username
    ])
    async def test_get_another_user(self, authenticated_ac: AsyncClient, username: str, email: EmailStr, status_code: int):
        """ Test get another User profile

        Args:
            authenticated_ac (AsyncClient): User
            username (str): User name
            email (EmailStr): User email
            status_code (int): test status_code
        """
        response = await authenticated_ac.get(f'/profile/@{username}')  # HTTP GET
        response_data = {key: value for key, value in response.json().items() if key != 'registred_at'}
        
        assert response.status_code == status_code
        if email:
            assert response_data == {
                'email': email,
                'username': username,
                'role_id': 1,
                'is_active': True,
                'projects': [],
                'user_tasks': [],
            }
    
    
    async def test_logout_current_user(self, authenticated_ac: AsyncClient, ac: AsyncClient):
        """ Test logout User

        Args:
            authenticated_ac (AsyncClient): Authenticated User
            ac (AsyncClient): Not authenticated User
        """
        response1 = await authenticated_ac.post('/profile/logout')  # HTTP POST
        response2 = await ac.post('/profile/logout')  # HTTP POST
        
        response1_data = response1.json()
        
        assert response1.status_code == 200
        assert response1_data == {'message': 'User successfully logged out', 'status_code': 200}
        assert response1.cookies.get('user_access_token') == None
        
        assert response2.status_code == 401
        assert response2.cookies.get('user_access_token') == None
    
    
    async def test_delete_current_user(self, authenticated_ac: AsyncClient, ac: AsyncClient):
        """ Test deleting User

        Args:
            authenticated_ac (AsyncClient): Authenticated User
            ac (AsyncClient): Not authenticated User
        """
        response1 = await authenticated_ac.post('/profile/login', json={  # HTTP POST. Re-login main User (test1)
            'email': 'test1@example.com',
            'password': 'test1'
        })
        response1 = await authenticated_ac.delete('/profile/delete_account')  # HTTP DELETE
        response2 = await ac.delete('/profile/delete_account')  # HTTP DELETE
        
        response1_data = response1.json()
        
        assert response1.status_code == 200
        assert response1_data == {'message': 'User account has been deleted', 'status_code': 200}
        assert response1.cookies.get('user_access_token') == None
        
        assert response2.status_code == 401
        assert response2.cookies.get('user_access_token') == None
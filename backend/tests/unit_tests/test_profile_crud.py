# TEST Profile CRUD requests - TSTU1

import pytest

from src.schemas import RoleCreateSchema
from src.schemas import RoleUpdateSchema
from src.schemas import UserCreateSchema
from src.schemas import UserUpdateSchema
from src.repositories import RoleDAO
from src.repositories import UserDAO


class TestRoleCRUD:
    @pytest.mark.usefixtures('clear_roles')
    async def test_create_role(self, role_create: RoleCreateSchema, role_dao_test: RoleDAO):
        """ Test creating Role

        Args:
            role_create (RoleCreateSchema): Role creating Validation
            role_dao_test (RoleDAO): Role DAO service
        """
        result = await role_dao_test.create_role(role_create)
        assert result == {'message': 'Role has been created'}
    
    
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('role_id, response', [
        (1, "<Role: id = 1, name = test, permicions = ['None']>"),
        (2, 'None'),
        (3, 'None'),
    ])
    async def test_read_role(self, role_id: int, response: str, role_dao_test: RoleDAO):
        """ Test reading Role from Database

        Args:
            role_id (int): Role id in the Database
            response (str): test response
            role_dao_test (RoleDAO): Role DAO service
        """
        result = await role_dao_test.get_role(role_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('role_id, response', [
        (1, "<Role: id = 1, name = test_updated, permicions = ['updated']>"),
        (2, 'None'),
        (3, 'None')
    ])
    async def test_update_role(self, role_id: int, response: str, role_update: RoleUpdateSchema, role_dao_test: RoleDAO):
        """ Test updating Role

        Args:
            role_id (int): Role id in the Database
            response (str): test response
            role_update (RoleUpdateSchema): Role updating Validation
            role_dao_test (RoleDAO): Role DAO service
        """
        result = await role_dao_test.update_role(role_update, role_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('role_id, response', [
        (1, {'message': 'Role has been deleted'})
    ])
    async def test_delete_one_role(self, role_id: int, response: dict, role_dao_test: RoleDAO):
        """ Test deleting one Role

        Args:
            role_id (int): Role id in the Database
            response (dict): test response
            role_dao_test (RoleDAO): Role DAO service
        """
        result = await role_dao_test.delete_one_role(role_id)
        assert result == response
        
        
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    async def test_delete_all_roles(self, role_dao_test: RoleDAO):
        """ Test deleting all Roles

        Args:
            role_dao_test (RoleDAO): Role DAO service
        """
        result = await role_dao_test.delete_all_roles()
        assert result == {'message': 'All Roles have been deleted'}
        

class TestUserCRUD:
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    async def test_create_user(self, user_create: UserCreateSchema, user_dao_test: UserDAO):
        """ Test creating User

        Args:
            user_create (UserCreateSchema): User creating Validation
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.create_user(user_create)
        assert result == {'message': 'User has been created'}
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', f'<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>'),
        ('None@example.com', 'None'),
        ('123', 'None')
    ])
    async def test_get_user_by_email(self, user_email: str, response: str, user_dao_test: UserDAO):
        """ Test reading User by email from the Database

        Args:
            user_email (str): User email in the Database
            response (str): test response
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.get_user_by_email(user_email)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_id, response', [
        (1, f'<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>'),
        (2, 'None'),
        (3, 'None')
    ])
    async def test_get_user_by_id(self, user_id: str, response: str, user_dao_test: UserDAO):
        """ Test reading User by id from the Database

        Args:
            user_id (str): User id in the Database
            response (str): test response
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.get_user_by_id(user_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_name, response', [
        ('test1', f'<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>'),
        ('None', 'None'),
        ('DROP TABLE user', 'None')
    ])
    async def test_get_user_by_name(self, user_name: str, response: str, user_dao_test: UserDAO):
        """ Test reading User by name from the Database

        Args:
            user_name (str): User name in the Database
            response (str): test response
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.get_user_by_name(user_name)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', f'<User: id = 1, username = test1_updated, email = testupdated@example.com, password = updated, role_id = 1, is_active = True>'),
        ('None@example.com', 'None'),
        ('abc', 'None')
    ])
    async def test_update_user(self, user_email: str, response: str, user_update: UserUpdateSchema, user_dao_test: UserDAO):
        """ Test updating User

        Args:
            user_email (str): User email in the Database
            response (str): test response
            user_update (UserUpdateSchema): User update Validation
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.update_user(user_update, user_email)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', {'message': 'User has been deleted'})
    ])
    async def test_delete_one_user(self, user_email: str, response: dict, user_dao_test: UserDAO):
        """ Test deleting one User

        Args:
            user_email (str): User email in the Database
            response (dict): test response
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.delete_one_user(user_email)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    async def test_delete_all_users(self, user_dao_test: UserDAO):
        """ Test deleting all Users

        Args:
            user_dao_test (UserDAO): User DAO service
        """
        result = await user_dao_test.delete_all_users()
        assert result == {'message': 'All Users have been deleted'}

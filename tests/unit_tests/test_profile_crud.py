import pytest

from src.schemas.role_schemas import RoleCreate, RoleUpdate
from src.schemas.user_schemas import UserCreate, UserUpdate
from src.repositories.role_service import RoleService
from src.repositories.user_service import UserService


class TestRoleCRUD:
    @pytest.mark.usefixtures('clear_roles')
    @pytest.mark.parametrize('response', [
        ({'message': 'Role has been created'})
    ])
    async def test_create_role(self, response: dict, role_create: RoleCreate, role_service_test: RoleService):
        result = await role_service_test.create_role(role_create)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('role_id, response', [
        (1, "<Role: id = 1, name = test, permicions = ['None']>"),
        (2, 'None'),
        (3, 'None')
    ])
    async def test_read_role(self, role_id: int, response: str, role_service_test: RoleService):
        result = await role_service_test.get_role(role_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('role_id, response', [
        (1, "<Role: id = 1, name = test_updated, permicions = ['updated']>"),
        (2, 'None'),
        (3, 'None')
    ])
    async def test_update_role(self, role_id: int, response: str, role_update: RoleUpdate, role_service_test: RoleService):
        result = await role_service_test.update_role(role_update, role_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('role_id, response', [
        (1, {'message': 'Role has been deleted'})
    ])
    async def test_delete_one_role(self, role_id: int, response: dict, role_service_test: RoleService):
        result = await role_service_test.delete_one_role(role_id)
        assert result == response
        
        
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('response', [
        ({'message': 'All Roles have been deleted'})
    ])
    async def test_delete_all_roles(self, response: dict, role_service_test: RoleService):
        result = await role_service_test.delete_all_roles()
        assert result == response
        

class TestUserCRUD:
    @pytest.mark.usefixtures('clear_roles', 'create_role')
    @pytest.mark.parametrize('response', [
        ({'message': 'User has been created'})
    ])
    async def test_create_user(self, response: dict, user_create: UserCreate, user_service_test: UserService):
        result = await user_service_test.create_user(user_create)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', f'<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>'),
        ('None@example.com', 'None'),
        ('123', 'None')
    ])
    async def test_get_user_by_email(self, user_email: str, response: str, user_service_test: UserService):
        result = await user_service_test.get_user_by_email(user_email)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_id, response', [
        (1, f'<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>'),
        (2, 'None'),
        (3, 'None')
    ])
    async def test_get_user_by_id(self, user_id: str, response: str, user_service_test: UserService):
        result = await user_service_test.get_user_by_id(user_id)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_name, response', [
        ('test1', f'<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>'),
        ('None', 'None'),
        ('DROP TABLE user', 'None')
    ])
    async def test_get_user_by_name(self, user_name: str, response: str, user_service_test: UserService):
        result = await user_service_test.get_user_by_name(user_name)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', f'<User: id = 1, username = test1_updated, email = testupdated@example.com, password = updated, role_id = 1, is_active = True>'),
        ('None@example.com', 'None'),
        ('abc', 'None')
    ])
    async def test_update_user(self, user_email: str, response: str, user_update: UserUpdate, user_service_test: UserService):
        result = await user_service_test.update_user(user_update, user_email)
        assert str(result) == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', {'message': 'User has been deleted'})
    ])
    async def test_delete_one_user(self, user_email: str, response: dict, user_service_test: UserService):
        result = await user_service_test.delete_one_user(user_email)
        assert result == response
    
    
    @pytest.mark.usefixtures('clear_users', 'clear_roles', 'create_role', 'create_user')
    @pytest.mark.parametrize('response', [
        ({'message': 'All Users have been deleted'})
    ])
    async def test_delete_all_users(self, response: dict, user_service_test: UserService):
        result = await user_service_test.delete_all_users()
        assert result == response
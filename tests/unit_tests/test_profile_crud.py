import pytest

from src.schemas.role_schemas import RoleCreate, RoleUpdate
from src.schemas.user_schemas import UserCreate, UserUpdate
from src.repositories.role_service import RoleService
from src.repositories.user_service import UserService


#TODO
@pytest.mark.usefixtures('clear_roles')
class TestRoleCRUD:
    async def test_create_role(self, role_create: RoleCreate, role_service_test: RoleService):
        result = await role_service_test.create_role(role_create)
        assert result == {'message': 'Role has been created'}
    
    @pytest.mark.parametrize('role_id, response', [
        (1, "<Role: id = 1, name = test, permicions = ['None']>"),
    ])
    async def test_read_role(self, role_create: RoleCreate, role_id: int, response: str, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.get_role(role_id)
        assert str(result) == response
        
    @pytest.mark.parametrize('role_id, response', [
        (1, "<Role: id = 1, name = test_updated, permicions = ['updated']>"),
    ])
    async def test_update_role(self, role_create: RoleCreate, role_update: RoleUpdate, role_id: int, response: str, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.update_role(role_update, role_id)
        assert str(result) == response
        
    @pytest.mark.parametrize('role_id, response', [
        (1, {'message': 'Role has been deleted'})
    ])
    async def test_delete_one_role(self, role_create: RoleCreate, role_id: int, response: str, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.delete_one_role(role_id)
        assert result == response
        
    async def test_delete_all_roles(self, role_create: RoleCreate, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.delete_all_roles()
        assert result == {'message': 'All Roles have been deleted'}
        

#TODO
@pytest.mark.usefixtures('clear_users', 'clear_roles')
class TestUserCRUD:
    async def test_create_user(self, role_create: RoleCreate, user_create: UserCreate, role_service_test: RoleService, user_service_test: UserService):
        await role_service_test.create_role(role_create)
        result = await user_service_test.create_user(user_create)
        assert result == {'message': 'User has been created'}
    
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', f"<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>")
    ])
    async def test_get_user_by_email(self, role_service_test: RoleService, user_service_test: UserService, user_email: str, response: str, role_create: RoleCreate, user_create: UserCreate):
        await role_service_test.create_role(role_create)
        await user_service_test.create_user(user_create)
        result = await user_service_test.get_user_by_email(user_email)
        assert str(result) == response
    
    @pytest.mark.parametrize('user_id, response', [
        (1, f"<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>")
    ])
    async def test_get_user_by_id(self, role_service_test: RoleService, user_service_test: UserService, user_id: str, response: str, role_create: RoleCreate, user_create: UserCreate):
        await role_service_test.create_role(role_create)
        await user_service_test.create_user(user_create)
        result = await user_service_test.get_user_by_id(user_id)
        assert str(result) == response
    
    @pytest.mark.parametrize('user_name, response', [
        ('test1', f"<User: id = 1, username = test1, email = test@example.com, password = test1, role_id = 1, is_active = True>")
    ])
    async def test_get_user_by_name(self, role_service_test: RoleService, user_service_test: UserService, user_name: str, response: str, role_create: RoleCreate, user_create: UserCreate):
        await role_service_test.create_role(role_create)
        await user_service_test.create_user(user_create)
        result = await user_service_test.get_user_by_name(user_name)
        assert str(result) == response
    
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', f"<User: id = 1, username = test1_updated, email = testupdated@example.com, password = updated, role_id = 1, is_active = True>")
    ])
    async def test_update_user(self, role_service_test: RoleService, user_service_test: UserService, user_email: str, response: str, role_create: RoleCreate, user_create: UserCreate, user_update: UserUpdate):
        await role_service_test.create_role(role_create)
        await user_service_test.create_user(user_create)
        result = await user_service_test.update_user(user_update, user_email)
        assert str(result) == response
    
    @pytest.mark.parametrize('user_email, response', [
        ('test@example.com', {'message': 'User has been deleted'})
    ])
    async def test_delete_one_user(self, role_service_test: RoleService, user_service_test: UserService, user_email: str, response: str, role_create: RoleCreate, user_create: UserCreate):
        await role_service_test.create_role(role_create)
        await user_service_test.create_user(user_create)
        result = await user_service_test.delete_one_user(user_email)
        assert result == response
    
    async def test_delete_all_users(self, role_service_test: RoleService, user_service_test: UserService, role_create: RoleCreate, user_create: UserCreate):
        await role_service_test.create_role(role_create)
        await user_service_test.create_user(user_create)
        result = await user_service_test.delete_all_users()
        assert result == {'message': 'All Users have been deleted'}
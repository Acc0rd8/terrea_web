import pytest

from src.schemas.role_schemas import RoleCreate, RoleUpdate
from src.repositories.role_service import RoleService


@pytest.mark.usefixtures('clear_roles')
class TestRoleCRUD:
    async def test_create_role(self, role_create: RoleCreate, role_service_test: RoleService):
        result = await role_service_test.create_role(role_create)
        assert result == {'message': 'Role has been created'}
    
    @pytest.mark.parametrize('role_id, response', [
        (2, "<Role: id = 2, name = test, permicions = ['None']>"),
    ])
    async def test_read_role(self, role_create: RoleCreate, role_id: int, response: str, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.get_role(role_id)
        assert str(result) == response
        
    @pytest.mark.parametrize('role_id, response', [
        (3, "<Role: id = 3, name = test_updated, permicions = ['updated']>"),
    ])
    async def test_update_role(self, role_create: RoleCreate, role_update: RoleUpdate, role_id: int, response: str, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.update_role(role_update, role_id)
        assert str(result) == response
        
    @pytest.mark.parametrize('role_id, response', [
        (4, {'message': 'Role has been deleted'})
    ])
    async def test_delete_one_role(self, role_create: RoleCreate, role_id: int, response: str, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.delete_one_role(role_id)
        assert result == response
        
    async def test_delete_all_roles(self, role_create: RoleCreate, role_service_test: RoleService):
        await role_service_test.create_role(role_create)
        result = await role_service_test.delete_all_roles()
        assert result == {'message': 'All Roles have been deleted'}
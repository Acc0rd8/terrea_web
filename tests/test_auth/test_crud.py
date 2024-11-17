import pytest
from typing import Any
from sqlalchemy import select, update, insert, delete
from contextlib import nullcontext as does_not_raise
from sqlalchemy.exc import DataError, ProgrammingError

from src.auth.models import User, Role
from src.auth.schemas import UserUpdate, RoleUpdate
from tests.test_auth.conftest import TestUser, TestRole

from tests.conftest import session_test


#UNIT_TESTS
@pytest.mark.usefixtures('empty_users', 'empty_roles')
class TestUnitUserCRUD:
    def test_create_user(self, test_user: TestUser, test_role: TestRole):
        with session_test() as session:
            stmt_role = insert(Role).values(**test_role.model_dump())
            stmt_user = insert(User).values(**test_user.model_dump())
            session.execute(stmt_role)
            session.execute(stmt_user)
            session.commit()
        
            query = select(User).where(User.email==test_user.email)
            result = session.execute(query)
            user = result.scalars().all()
            
            assert str(user[0]) == f'<User: id = 1, username = test, email = test@example.com, password = test1, role_id = 1, is_active = True>', 'User was not created'

    
    @pytest.mark.parametrize(
        'user_old_email, expectation', 
        [
            ('test@example.com', does_not_raise()),
            ('string', pytest.raises(IndexError)),
            (1, pytest.raises(ProgrammingError)),
            ('DROP TABLE user', pytest.raises(IndexError)),
        ]
    )
    def test_update_user(self, test_user: TestUser, test_role: TestRole, user_update: UserUpdate, user_old_email: str, expectation: Exception | None):
        with expectation:
            with session_test() as session:
                stmt_role = insert(Role).values(**test_role.model_dump())
                stmt_user = insert(User).values(**test_user.model_dump())
                session.execute(stmt_role)
                session.execute(stmt_user)
                
                new_user_dict = user_update.model_dump(exclude_unset=True)
                stmt = update(User).where(User.email==user_old_email).values(new_user_dict).returning(User)
                result = session.execute(stmt)
                session.commit()
                user = result.scalars().all()
                assert str(user[0]) == '<User: id = 1, username = updated, email = updated@example.com, password = updated, role_id = 1, is_active = True>', 'User was not created'
    
    
    @pytest.mark.parametrize(
        'user_email, expectation',
        [
            ('test@example.com', does_not_raise()),
            (1, pytest.raises(ProgrammingError))
        ]
    )
    def test_delete_user(self, test_user: TestUser, test_role: TestRole, user_email: str, expectation: Exception | None):
        with expectation:
            with session_test() as session:
                stmt_role = insert(Role).values(**test_role.model_dump())
                stmt_user = insert(User).values(**test_user.model_dump())
                session.execute(stmt_role)
                session.execute(stmt_user)
                
                stmt_del = delete(User).where(User.email==user_email)
                session.execute(stmt_del)
                
                query = select(User)
                result = session.execute(query)
                user = result.one_or_none()
                session.commit()

                assert user == None, 'User was not deleted'


@pytest.mark.usefixtures('empty_users', 'empty_roles')
class TestUnitRoleCRUD:
    def test_create_role(self, test_role: TestRole):
        with session_test() as session:
            stmt = insert(Role).values(**test_role.model_dump())
            session.execute(stmt)
            session.commit()
            
            query = select(Role)
            result = session.execute(query)
            user = result.scalars().all()
            
            assert str(user[0]) == f"<Role: id = 1, name = user, permicions = ['None']>", 'Role was not created'
    
    
    @pytest.mark.parametrize(
        'role_old_id, expectation',
        [
            (1, does_not_raise()),
            (2, pytest.raises(IndexError)),
            ('text', pytest.raises(DataError))
        ]
    )
    def test_update_role(self, test_role: TestRole, role_update: RoleUpdate, role_old_id: int, expectation: Exception | None):
        with expectation:
            with session_test() as session:
                stmt = insert(Role).values(**test_role.model_dump())
                session.execute(stmt)
                
                new_role_dict = role_update.model_dump()
                stmt = update(Role).where(Role.id==role_old_id).values(new_role_dict).returning(Role)
                result = session.execute(stmt)
                session.commit()
                
                role = result.scalars().all()
                
                assert str(role[0]) == f"<Role: id = 1, name = user, permicions = ['SomeUpdate']>", 'Role was not updated'
                
    
    @pytest.mark.parametrize(
        'role_id, expectation',
        [
            (1, does_not_raise()),
            ('text', pytest.raises(DataError))
        ]
    )
    def test_delete_role(self, test_role: TestRole, role_id: int, expectation: Exception | None):
        with expectation:
            with session_test() as session:
                stmt_add_role = insert(Role).values(**test_role.model_dump())
                session.execute(stmt_add_role)
                
                stmt_del_role = delete(Role).where(Role.id==role_id)
                session.execute(stmt_del_role)
                
                query = select(Role)
                result = session.execute(query)
                role = result.one_or_none()
                session.commit()
                
                assert role == None, 'Role was not deleted'
            
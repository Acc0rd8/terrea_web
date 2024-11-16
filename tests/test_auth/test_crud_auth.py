import pytest
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import nullcontext as does_not_raise

from src.auth.schemas import UserCreate, UserUpdate
from src.auth.models import User, Role

from tests.conftest import async_session_test
    

@pytest.mark.usefixtures('empty_users', 'empty_roles')
class TestUserCRUD:
    async def test_create_user(self, user_create: UserCreate):
        async with async_session_test() as session:
            stmt_role = insert(Role).values(id=1, name='user', permicions=['None'])
            stmt_user = insert(User).values(**user_create.model_dump())
            await session.execute(stmt_role)
            await session.execute(stmt_user)
            await session.commit()
        
            query = select(User).where(User.email==user_create.email)
            result = await session.execute(query)
            user = result.scalars().all()
            
            assert str(user[0]) == '<User: id = 1, username = test, email = test@example.com, password = test1, role_id = 1, is_active = True>', 'User was not created'
        
    #TODO
    async def test_get_users(self):
        pass

    
    @pytest.mark.parametrize(
        'user_old_email, expectation', 
        [
            ('test@example.com', does_not_raise()),
            ('string', pytest.raises(IndexError)),
            (str(1), pytest.raises(IndexError)),
            ('DROP TABLE user', pytest.raises(IndexError))
        ]
    )
    async def test_update_user(self, user_update: UserUpdate, user_old_email: str, expectation):
        with expectation:
            async with async_session_test() as session:
                stmt_role = insert(Role).values(id=1, name='user', permicions=['None'])
                stmt_user = insert(User).values(username='test', email='test@example.com', password='test1')
                await session.execute(stmt_role)
                await session.execute(stmt_user)
                await session.flush()
                
                new_user_dict = user_update.model_dump(exclude_unset=True)
                stmt = update(User).where(User.email==user_old_email).values(new_user_dict).returning(User)
                result = await session.execute(stmt)
                await session.commit()
                user = result.scalars().all()
                assert str(user[0]) == '<User: id = 2, username = updated, email = updated@example.com, password = updated, role_id = 1, is_active = True>', 'User was not created'
    
         
    async def test_delete_user(user_email: str, expectation):
        with expectation:
            async with async_session_test() as session:
                stmt = delete(User).where(User.email==user_email)
                result = await session.execute(stmt)
                await session.commit()
                
                assert result.one_or_none() == None


@pytest.mark.usefixtures('empty_roles')
class TestRoleCRUD:
    pass

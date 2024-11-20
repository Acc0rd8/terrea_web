'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.profile.models import User
from src.profile.schemas import UserCreate, UserUpdate
from src.database import async_session


#CREATE
async def create_user(user_in: UserCreate, session: AsyncSession) -> dict:
    stmt = insert(User).values(**user_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'message': 'User has been created'}


#READ
async def get_user(user_email: str, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.email==user_email)
    result = await session.execute(stmt)
    user = result.scalar()
    return user
    
    
#UPDATE
async def update_user(new_user: UserUpdate, user_old_email: str, session: AsyncSession) -> User:
    new_user_dict = new_user.model_dump(exclude_unset=True)
    stmt = update(User).where(User.email==user_old_email).values(new_user_dict).returning(User)
    result = await session.execute(stmt)
    await session.commit()
    user = result.scalar()
    return user
    

#DELETE
async def delete_user(user_email: str, session: AsyncSession) -> dict:
    stmt = delete(User).where(User.email==user_email)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'User has been deleted'}
    

async def delete_all_users(session: AsyncSession) -> dict:
    stmt = delete(User)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Deleted'}

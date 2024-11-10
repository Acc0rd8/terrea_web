'''
Create
Read
Update
Delete
'''

from fastapi import Depends
from sqlalchemy import select, update, insert, delete

from ..database import async_session
from ..models.user_and_role import User
from ..auth.schemas import UserCreate, UserUpdate


#CREATE
async def create_user(user_in: UserCreate) -> dict:
    async with async_session() as session:
        stmt = insert(User).values(**user_in.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {'message': 'success'}


#READ
async def get_user(user_email: str) -> User | None:
    async with async_session() as session:
        stmt = select(User).where(User.email==user_email)
        result = await session.execute(stmt)
        user = result.scalars().all()
        return user[0]
    
    
#UPDATE
async def update_user(new_user: UserUpdate, user_old_email: str) -> User:
    async with async_session() as session:
        new_user_dict = new_user.model_dump(exclude_unset=True)
        stmt = update(User).where(User.email==user_old_email).values(new_user_dict).returning(User)
        result = await session.execute(stmt)
        await session.commit()
        user = result.scalars().all()
        return user[0]

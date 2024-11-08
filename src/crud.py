'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete
from fastapi import Depends

from .database import async_session
from .models.user_and_role import User
from .auth.schemas import UserCreate


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
        return user
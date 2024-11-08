'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import Depends

from typing import Annotated

from .database import create_async_engine
from .models.user_and_role import User
from .auth.schemas import UserCreate


session_db = Annotated[async_sessionmaker, Depends(create_async_engine)]


#CREATE
async def create_user(user_in: UserCreate, session: AsyncSession = session_db) -> dict:
    stmt = insert(User).values(**(user_in.model_dump()))
    await session.execute(stmt)
    await session.commit()
    return {'message': 'success'}


#READ
async def get_user(user_email: str, session: AsyncSession = session_db) -> User | None:
    stmt = select(User).where(User.email==user_email)
    result = await session.execute(stmt)
    user = result.scalars()
    return user
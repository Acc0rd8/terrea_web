'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete

from src.database import async_session
from src.models.user_and_role import User
from src.auth.schemas import UserCreate, UserUpdate


#CREATE
async def create_user(user_in: UserCreate) -> dict:
    async with async_session() as session:
        stmt = insert(User).values(**user_in.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {'message': 'User has been created'}


#READ
async def get_user(user_email: str) -> User | None:
    async with async_session() as session:
        stmt = select(User).where(User.email==user_email)
        result = await session.execute(stmt)
        user = result.scalar()
        return user
    
    
#UPDATE
async def update_user(new_user: UserUpdate, user_old_email: str) -> User:
    async with async_session() as session:
        new_user_dict = new_user.model_dump(exclude_unset=True)
        stmt = update(User).where(User.email==user_old_email).values(new_user_dict).returning(User)
        result = await session.execute(stmt)
        await session.commit()
        user = result.scalar()
        return user
    

#DELETE
async def delete_user(user_email: str) -> dict:
    async with async_session() as session:
        stmt = delete(User).where(User.email==user_email)
        await session.execute(stmt)
        await session.commit()
        return {'message': 'User has been deleted'}

'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Role
from src.auth.schemas import RoleCreate, RoleUpdate
from src.database import async_session


#CREATE
async def create_role(role_in: RoleCreate, session: AsyncSession) -> dict:
    stmt = insert(Role).values(**role_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Role has been created'}


#READ
async def get_role(role_id: int, session: AsyncSession) -> Role | None:
    stmt = select(Role).where(Role.id==role_id)
    result = await session.execute(stmt)
    role = result.scalar()
    return role


#UPDATE
async def update_role(new_role: RoleUpdate, role_old_id: int, session: AsyncSession) -> Role:
    new_role_dict = new_role.model_dump(exclude_unset=True)
    stmt = update(Role).where(Role.id==role_old_id).values(new_role_dict).returning(Role)
    result = await session.execute(stmt)
    role = result.scalar()
    await session.commit()
    return role


#DELETE
async def delete_role(role_id: int, session: AsyncSession) -> dict:
    stmt = delete(Role).where(Role.id==role_id)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Role has been deleted'}


async def delete_all_roles(session: AsyncSession) -> dict:
    stmt = delete(Role)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Deleted'}
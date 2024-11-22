'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.projects.models import Task
from src.projects.schemas import TaskCreate, TaskUpdate

#CREATE
async def create_task(task_in: TaskCreate, session: AsyncSession) -> dict:
    stmt = insert(Task).values(**task_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Task has been created'}


#READ
async def get_task(task_id: int, session: AsyncSession) -> Task | None:
    query = select(Task).where(Task.id==task_id)
    result = await session.execute(query)
    task = result.scalar()
    return task


#UPDATE
async def update_task(new_task: TaskUpdate, old_task_id: int, session: AsyncSession) -> Task:
    new_task_dict = new_task.model_dump(exclude_unset=True)
    stmt = update(Task).where(Task.id==old_task_id).values(new_task_dict).returning(Task)
    result = await session.execute(stmt)
    await session.commit()
    task = result.scalar()
    return task


#DELETE
async def delete_task(task_id: int, session: AsyncSession) -> dict:
    stmt = delete(Task).where(Task.id==task_id)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Task has been deleted'}

async def delete_all_tasks(session: AsyncSession) -> dict:
    stmt = delete(Task)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'All tasks have been deleted'}
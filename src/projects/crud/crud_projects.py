'''
Create
Read
Update
Delete
'''

from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.projects.models import Project
from src.projects.schemas import ProjectCreate, ProjectUpdate

#CREATE
async def create_project(project_in: ProjectCreate, session: AsyncSession) -> dict:
    stmt = insert(Project).values(**project_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Project has been created'}


#READ
async def get_project(project_id: int, session: AsyncSession) -> Project | None:
    query = select(Project).where(Project.id==project_id)
    result = await session.execute(query)
    project = result.scalar()
    return project


#UPDATE
async def update_project(new_project: ProjectUpdate, old_project_id: int, session: AsyncSession) -> Project:
    new_project_dict = new_project.model_dump(exclude_unset=True)
    stmt = update(Project).where(Project.id==old_project_id).values(new_project_dict).returning(Project)
    result = await session.execute(stmt)
    await session.commit()
    project = result.scalar()
    return project


#DELETE
async def delete_project(project_id: int, session: AsyncSession) -> dict:
    stmt = delete(Project).where(Project.id==project_id)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Project has been deleted'}

async def delete_all_projects(session: AsyncSession) -> dict:
    stmt = delete(Project)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'All projects have been deleted'}
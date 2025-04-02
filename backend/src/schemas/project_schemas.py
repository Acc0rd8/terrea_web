from datetime import datetime

from pydantic import Field

from src.schemas.base_schema import BaseSchema
from src.schemas.task_schemas import TaskReadSchema


class ProjectBaseSchema(BaseSchema):
    pass


class ProjectCreateSchema(ProjectBaseSchema):
    name: str = Field(min_length=3, max_length=50)

    
class ProjectReadSchema(ProjectBaseSchema):
    id: int
    name: str
    created_at: datetime
    owner_id: int
    project_tasks: list[TaskReadSchema] # List of Project Tasks (Model TaskRead)
    

class ProjectUpdateSchema(ProjectBaseSchema):
    name: str = Field(min_length=3, max_length=50)
    

class ProjectDeleteSchema(ProjectBaseSchema):
    name: str

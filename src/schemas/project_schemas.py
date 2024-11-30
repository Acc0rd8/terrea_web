from pydantic import Field
from datetime import datetime

from src.schemas.base_schema import BaseSchema
from src.schemas.task_schemas import TaskRead


class ProjectBase(BaseSchema):
    pass


class ProjectCreate(ProjectBase):
    name: str = Field(min_length=3, max_length=50)

    
class ProjectRead(ProjectBase):
    id: int
    name: str
    created_at: datetime
    owner_id: int
    project_tasks: list[TaskRead]
    

class ProjectUpdate(ProjectBase):
    name: str = Field(min_length=3, max_length=50)
    

class ProjectDelete(ProjectBase):
    name: str

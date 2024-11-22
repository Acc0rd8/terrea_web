from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


#PROJECT
class ProjectBase(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}


class ProjectCreate(ProjectBase):
    name: str = Field(min_length=3, max_length=50)

    
class ProjectRead(ProjectBase):
    id: int
    name: str
    created_at: datetime
    tasks: list
    

class ProjectUpdate(ProjectBase):
    name: str = Field(min_length=3, max_length=50)
    

class ProjectDelete(ProjectBase):
    name: str
    

#TASK
class TaskBase(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}
    

class TaskCreate(TaskBase):
    name: str = Field(min_length=3, max_length=100)
    deadline: Optional[datetime]
    

class TaskRead(TaskBase):
    id: int
    name: str
    project_id: int
    created_at: datetime
    updated_at: datetime
    deadline: Optional[datetime]
    project: str
    

class TaskUpdate(TaskBase):
    name: str
    deadline: Optional[datetime]
    

class TaskDelete(TaskBase):
    id: int
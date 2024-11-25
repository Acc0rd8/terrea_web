from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


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
    project_name: str
    created_at: datetime
    updated_at: datetime
    deadline: Optional[datetime]


class TaskUpdate(TaskBase):
    name: str
    deadline: Optional[datetime]
    

class TaskDelete(TaskBase):
    id: int
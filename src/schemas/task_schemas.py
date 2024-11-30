from pydantic import Field
from datetime import date, datetime
from typing import Optional

from src.schemas.base_schema import BaseSchema


class TaskBase(BaseSchema):
    pass
    

class TaskCreate(TaskBase):
    customer_id: int
    performer_id: int
    name: str = Field(min_length=3, max_length=100)
    deadline: Optional[date]
    

class TaskRead(TaskBase):
    id: int
    name: str
    customer_id: int
    performer_id: int
    created_at: datetime
    updated_at: datetime
    deadline: Optional[date]


class TaskUpdate(TaskBase):
    name: str = Field(min_length=3, max_length=100)
    deadline: Optional[datetime]
    

class TaskDelete(TaskBase):
    id: int
from datetime import date, datetime
from typing import Optional

from pydantic import Field

from src.schemas.base_schema import BaseSchema


class TaskBase(BaseSchema): # Base Task Schema
    pass
    

class TaskCreate(TaskBase):
    customer_id: int
    performer_id: int
    name: str = Field(min_length=3, max_length=100)
    deadline: Optional[date] # If deadline exists - date, else None
    

class TaskRead(TaskBase): # Show info about Task
    id: int
    name: str
    customer_id: int
    performer_id: int
    created_at: datetime
    updated_at: datetime
    deadline: Optional[date] # If deadline exists - date, else None


class TaskUpdate(TaskBase):
    name: str = Field(min_length=3, max_length=100)
    deadline: Optional[date] # If deadline exists - date, else None
    

class TaskDelete(TaskBase):
    id: int

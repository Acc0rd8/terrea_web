from datetime import date, datetime
from typing import Optional

from pydantic import Field

from src.schemas.base_schema import BaseSchema


class TaskBaseSchema(BaseSchema):
    pass
    

class TaskCreateSchema(TaskBaseSchema):
    customer_name: str
    performer_name: str
    name: str = Field(min_length=3, max_length=50)
    deadline: Optional[date] # If deadline exists - date, else None
    

class TaskReadSchema(TaskBaseSchema):
    id: int
    name: str
    customer_name: str
    performer_name: str
    created_at: datetime
    updated_at: datetime
    deadline: Optional[date] # If deadline exists - date, else None


class TaskUpdateSchema(TaskBaseSchema):
    name: str = Field(min_length=3, max_length=100)
    deadline: Optional[date] # If deadline exists - date, else None
    

class TaskDeleteSchema(TaskBaseSchema):
    id: int

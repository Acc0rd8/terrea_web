from pydantic import BaseModel, EmailStr, Field 
from datetime import datetime
from typing import Union

from src.schemas.project_schemas import ProjectRead
from src.schemas.task_schemas import TaskRead


class UserBase(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}


class UserCreate(UserBase): 
    username: str = Field(min_length=3, max_length=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str = Field(min_length=5) #Password (length >= 5 symbols)
    

class UserAuth(UserBase):
    email: EmailStr
    password: str


class UserRead(UserBase):
    username: str
    email: EmailStr
    registred_at: Union[str, datetime]
    role_id: int
    is_active: bool
    projects: list[ProjectRead]
    user_tasks: list[TaskRead]


class UserUpdate(UserBase):
    username: str = Field(min_length=3, max_length=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str = Field(min_length=5)
    is_active: bool = Field(default=True)


class UserDelete(UserBase):
    email: EmailStr

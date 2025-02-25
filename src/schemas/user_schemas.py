from datetime import datetime
from typing import Union

from pydantic import EmailStr, Field

from src.schemas.base_schema import BaseSchema
from src.schemas.project_schemas import ProjectRead
from src.schemas.task_schemas import TaskRead


class UserBase(BaseSchema): # Base User Schema
    email: EmailStr


class UserCreate(UserBase): # Register
    username: str = Field(min_length=3, max_length=20) # Username (length >= 3 symbols) and (length <= 20 symbols)
    password: str = Field(min_length=5) # Password (length >= 5 symbols)
    

class UserAuth(UserBase): # Login
    password: str


class UserRead(UserBase): # Show info about User
    username: str
    registred_at: Union[str, datetime]
    role_id: int
    is_active: bool # If User is active on site => is_active = True, else False
    projects: list[ProjectRead] # List of User Project (Model ProjectRead)
    user_tasks: list[TaskRead] # List of User Tasks (Model TaskRead)


class UserUpdate(UserBase): # Update
    username: str = Field(min_length=3, max_length=20) # Username (length >= 3 symbols) and (length <= 20 symbols)
    password: str = Field(min_length=5) # Password (length >= 5 symbols)
    is_active: bool = Field(default=True)


class UserDelete(UserBase): # Delete
    pass

from datetime import datetime
from typing import Union

from pydantic import EmailStr, Field

from src.schemas.base_schema import BaseSchema
from src.schemas.project_schemas import ProjectReadSchema
from src.schemas.task_schemas import TaskReadSchema


class UserBaseSchema(BaseSchema):
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    username: str = Field(min_length=3, max_length=20) # Username (length >= 3 symbols) and (length <= 20 symbols)
    password: str = Field(min_length=5) # Password (length >= 5 symbols)
    

class UserAuthSchema(UserBaseSchema):
    password: str


class UserReadSchema(UserBaseSchema):
    username: str
    registred_at: Union[str, datetime]
    role_id: int
    is_active: bool # If User is active on site => is_active = True, else False
    projects: list[ProjectReadSchema] # List of User Project (Model ProjectRead)
    user_tasks: list[TaskReadSchema] # List of User Tasks (Model TaskRead)


class UserUpdateSchema(UserBaseSchema):
    username: str = Field(min_length=3, max_length=20) # Username (length >= 3 symbols) and (length <= 20 symbols)
    password: str = Field(min_length=5) # Password (length >= 5 symbols)
    is_active: bool = Field(default=True)


class UserDeleteSchema(UserBaseSchema):
    pass

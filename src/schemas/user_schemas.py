from pydantic import BaseModel, EmailStr, Field 
from datetime import datetime
from typing import Union

from src.schemas.project_schemas import ProjectRead

class UserCreate(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, password)
    model_config = {'from_attributes': True}
    
    username: str = Field(min_length=3, max_length=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str = Field(min_length=5) #Password (length >= 5 symbols)
    

class UserAuth(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}
    
    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, registred_at, role_id, is_active)
    model_config = {'from_attributes': True}
    
    username: str
    email: EmailStr
    registred_at: Union[str, datetime]
    role_id: int
    is_active: bool
    projects: list[ProjectRead]


class UserUpdate(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, password)
    model_config = {'from_attributes': True}
    
    username: str = Field(min_length=3, max_length=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str = Field(min_length=5)
    is_active: bool = Field(default=True)


class UserDelete(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (email)
    model_config = {'from_attributes': True}
    
    email: EmailStr

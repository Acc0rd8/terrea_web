from pydantic import BaseModel, EmailStr, Field 


class UserCreate(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, password)
    
    username: str = Field(ge=3, le=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str = Field(ge=5) #Password (length >= 5 symbols)
    

class UserRead(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, registred_at, role_id, is_active)
    
    username: str
    email: EmailStr
    registred_at: str
    role_id: int
    is_active: bool


class UserUpdate(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, password)
    
    username: str = Field(ge=3, le=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str


class UserDelete(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (email)
    
    email: EmailStr
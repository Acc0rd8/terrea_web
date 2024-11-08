from pydantic import BaseModel, EmailStr, Field 


#USER
class UserCreate(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, password)
    
    username: str = Field(min_length=3, max_length=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str = Field(min_length=5) #Password (length >= 5 symbols)
    

class UserAuth(BaseModel):
    model_config = {'extra': 'forbid'}
    
    email: EmailStr
    password: str

class UserRead(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, registred_at, role_id, is_active)
    
    username: str
    email: EmailStr
    registred_at: str
    role_id: int
    is_active: bool


class UserUpdate(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (username, email, password)
    
    username: str = Field(min_length=3, max_length=20) #Username (length >= 3 symbols) and (length <= 20 symbols)
    email: EmailStr
    password: str


class UserDelete(BaseModel):
    model_config = {'extra': 'forbid'} #Forbid extra field except (email)
    
    email: EmailStr
    

#TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: int
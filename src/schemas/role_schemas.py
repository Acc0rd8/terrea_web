from pydantic import BaseModel


class RoleCreate(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}
    
    name: str
    permicions: list[str]


class RoleRead(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}
    
    id: int
    name: str
    permicions: list[str]


class RoleUpdate(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}
    
    permicions: list[str]


class RoleDelete(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}
    
    name: str

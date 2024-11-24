from pydantic import BaseModel, Field
from datetime import datetime



class ProjectBase(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}


class ProjectCreate(ProjectBase):
    
    name: str = Field(min_length=3, max_length=50)

    
class ProjectRead(ProjectBase):
    id: int
    name: str
    created_at: datetime
    tasks: list
    owner_id: int
    

class ProjectUpdate(ProjectBase):
    name: str = Field(min_length=3, max_length=50)
    

class ProjectDelete(ProjectBase):
    name: str

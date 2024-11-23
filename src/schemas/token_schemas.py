from pydantic import BaseModel


class Token(BaseModel):
    model_config = {'extra': 'forbid'}
    
    access_token: str
    token_type: str
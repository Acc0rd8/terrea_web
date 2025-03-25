from pydantic import BaseModel


class BaseSchema(BaseModel):
    model_config = {'extra': 'forbid'} # Forbid Extra fields
    model_config = {'from_attributes': True} # Allow to Convert SQLAlchemy model to Pydantic model

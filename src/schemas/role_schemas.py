from pydantic import BaseModel


class RoleBase(BaseModel):
    model_config = {'extra': 'forbid'}
    model_config = {'from_attributes': True}


class RoleCreate(RoleBase):
    name: str
    permicions: list[str]


class RoleRead(RoleBase):
    id: int
    name: str
    permicions: list[str]


class RoleUpdate(RoleBase):
    permicions: list[str]


class RoleDelete(RoleBase):
    name: str

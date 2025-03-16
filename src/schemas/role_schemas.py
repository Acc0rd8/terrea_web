from src.schemas.base_schema import BaseSchema


class RoleBase(BaseSchema):
    name: str


class RoleCreate(RoleBase):
    permicions: list[str] # List of User permicions


class RoleRead(RoleBase):
    id: int
    permicions: list[str] # List of User permicions


class RoleUpdate(RoleBase):
    permicions: list[str] # List of User permicions


class RoleDelete(RoleBase):
    pass

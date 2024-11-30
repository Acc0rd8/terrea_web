from src.schemas.base_schema import BaseSchema


class RoleBase(BaseSchema):
    name: str


class RoleCreate(RoleBase):
    permicions: list[str]


class RoleRead(RoleBase):
    id: int
    permicions: list[str]


class RoleUpdate(RoleBase):
    permicions: list[str]


class RoleDelete(RoleBase):
    pass

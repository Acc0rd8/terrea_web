from src.schemas.base_schema import BaseSchema


class RoleBaseSchema(BaseSchema):
    name: str


class RoleCreateSchema(RoleBaseSchema):
    permicions: list[str] # List of User permicions


class RoleReadSchema(RoleBaseSchema):
    id: int
    permicions: list[str] # List of User permicions


class RoleUpdateSchema(RoleBaseSchema):
    permicions: list[str] # List of User permicions


class RoleDeleteSchema(RoleBaseSchema):
    pass

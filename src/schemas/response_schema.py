from src.schemas.base_schema import BaseSchema


class ResponseSchema(BaseSchema):
    status_code: int
    message: bool

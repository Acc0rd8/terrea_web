from src.schemas.base_schema import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str
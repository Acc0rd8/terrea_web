from src.schemas.base_schema import BaseSchema


class Token(BaseSchema):
    access_token: str # Encoded {'sub': str, 'exp': datetime}
    token_type: str # Token type (cookie)

from src.schemas.base_schema import BaseSchema


class Token(BaseSchema): # Base Token Schema
    access_token: str # encoded {'sub': str, 'exp': datetime}
    token_type: str # Token type (cookie)
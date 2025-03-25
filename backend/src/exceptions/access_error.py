from fastapi import status

from src.exceptions.custom_error import CustomError


class AccessError(CustomError):
    """
    Action access Error
    """
    
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, message=msg)

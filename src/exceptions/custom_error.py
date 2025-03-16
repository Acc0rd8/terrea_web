class CustomError(Exception):
    """
    General class of customs exceptions
    """
    
    def __init__(self, status_code: int, message: str):
        self._status_code = status_code
        self._message = message
        
    @property
    def code(self) -> int:
        return self._status_code
    
    @property
    def message(self) -> str:
        return self._message
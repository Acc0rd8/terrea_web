from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """
    App settings
    """
    
    model_config = SettingsConfigDict(env_file='.env')
    
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def TEST_DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
    
    @property
    def DATABASE_INFO(self) -> dict:
        return {
            'DB_USER': self.DB_USER,
            'DB_PASS': self.DB_PASS,
            'DB_HOST': self.DB_HOST,
            'DB_PORT': self.DB_PORT,
            'DB_NAME': self.DB_NAME,
        }
    
    @property
    def TEST_DATABASE_INFO(self) -> dict:
        return {
            'DB_USER_TEST': self.DB_USER_TEST,
            'DB_PASS_TEST': self.DB_PASS_TEST,
            'DB_HOST_TEST': self.DB_HOST_TEST,
            'DB_PORT_TEST': self.DB_PORT_TEST,
            'DB_NAME_TEST': self.DB_NAME_TEST,
        }
    
    @property
    def AUTH_DATA(self) -> dict:
        return {'secret_key': self.SECRET_KEY, 'algorithm': self.ALGORITHM}
    
    @property
    def ACCESS_TOKEN_EXPIRE_DAYS(self) -> str:
        return f'{self.ACCESS_TOKEN_EXPIRE_DAYS}'
    

settings = Settings()

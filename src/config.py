from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def AUTH_DATA(self) -> dict:
        return {'secret_key': self.SECRET_KEY, 'algorithm': self.ALGORITHM}
    
    @property
    def ACCESS_TOKEN_EXPIRE_DAYS(self) -> str:
        return f'{self.ACCESS_TOKEN_EXPIRE_DAYS}'
    

settings = Settings()
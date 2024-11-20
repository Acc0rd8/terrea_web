from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str
    
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def TEST_SYNC_DATABASE_URL(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'
    
    @property
    def TEST_ASYNC_DATABASE_URL(self) -> str:
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
    def AUTH_DATA(self) -> dict:
        return {'secret_key': self.SECRET_KEY, 'algorithm': self.ALGORITHM}
    
    @property
    def ACCESS_TOKEN_EXPIRE_DAYS(self) -> str:
        return f'{self.ACCESS_TOKEN_EXPIRE_DAYS}'
    

settings = Settings()
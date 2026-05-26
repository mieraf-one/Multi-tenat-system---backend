from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
    
settings = Settings()
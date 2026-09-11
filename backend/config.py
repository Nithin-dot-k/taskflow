from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskFlow API"
    DATABASE_URL: str 

     # Add JWT configurations:
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    model_config=SettingsConfigDict(env_file=".env",extra="ignore")

settings=Settings()
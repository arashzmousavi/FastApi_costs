from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "test"



settings = Settings()

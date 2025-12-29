from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "test"
    REDIS_URL: str
    SENTRY_DSN: str = "https://09f0d4024e83fbff921a122e95e8a94f@sentry.hamravesh.com/9577"



settings = Settings()

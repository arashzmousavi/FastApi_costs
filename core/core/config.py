from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///:memory:"
    JWT_SECRET_KEY: str = "test"
    REDIS_URL: str = "redis://redis:6379"
    CELERY_BROKER_URL: str = "redis://redis:6379/3"
    CELERY_BACKEND_URL: str = "redis://redis:6379/3"
    SENTRY_DSN: str = "https://09f0d4024e83fbff921a122e95e8a94f@sentry.hamravesh.com/9577"



settings = Settings()

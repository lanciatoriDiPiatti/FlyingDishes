from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/flying_dishes"
    
    # JWT configuration
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()

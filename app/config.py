from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALORITHM: str
    TOKEN_EXP: int

    class Config:
        env_file = ".env"

settings = Settings()
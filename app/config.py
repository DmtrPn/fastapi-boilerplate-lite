from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Example Service API"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8008
    WORKERS: int = 1
    DATABASE_URI: str = ""
    COOKIE_SECRET_KEY: str = "COOKIE_SECRET_KEY"
    COOKIE_NAME: str = "example"


settings = Settings()

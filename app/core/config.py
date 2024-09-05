from typing import List

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "API"
    API_V1_STR: str = "/api/v1"
    MODULE_NAME: str
    DEBUG: bool
    BACKEND_CORS_ORIGINS: List[str]

    APP_URL: AnyHttpUrl

    GEMINI_API_KEY: str
    GEMINI_MODEL: str

    WEATHER_API_KEY: str
    WEATHER_BASE_URL: str

    REDIS_PORT: int
    REDIS_DATABASE: int
    REDIS_HOST: str

    class ConfigDict:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()

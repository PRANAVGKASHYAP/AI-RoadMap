# this file is ment to load the settings from the .env file and do pydantic validation

# do the imports
from functools import lru_cache

from pydantic import SecretStr  # this is only to make the pasword printing hashed out
from pydantic_settings import BaseSettings, SettingsConfigDict

# make a class to represent the .env file


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LLM_API_KEY: SecretStr
    LLM_BASE_URL: str
    LOG_LEVEL: str = "INFO"


# addging  the lru cache
@lru_cache
def get_settings() -> Settings:
    return Settings()

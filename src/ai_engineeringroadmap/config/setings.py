# this file is ment to load the settings from the .env file and do pydantic validation

# do the imports
from pydantic import SecretStr  # this is only to make the pasword printing hashed out
from pydantic_settings import BaseSettings, SettingsConfigDict

# make a class to represent the .env file


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LLM_API_KEY: SecretStr
    LLM_BASE_URL: str
    LOG_LEVEL: str = "INFO"


settings = (
    Settings()
)  # this is because this object can be directly used in other classes

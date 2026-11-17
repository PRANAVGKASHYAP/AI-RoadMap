import pytest
from pydantic import ValidationError

from ai_engineeringroadmap.config.setings import Settings


def test_missing_key(monkeypatch):
    # Remove the LLM_API_KEY from the environment
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    # deleting the key manually for this run , should make th evalidatoin fail
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None
        )  # This should raise a ValidationError due to missing key


def test_valid_settings(monkeypatch):
    # Set a valid LLM_API_KEY in the environment
    monkeypatch.setenv("LLM_API_KEY", "test_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://api.example.com/v1")

    settings = Settings(_env_file=None)  # Load settings
    assert settings.LLM_API_KEY.get_secret_value() == "test_key"
    assert settings.LLM_BASE_URL == "https://api.example.com/v1"
    assert settings.LOG_LEVEL == "INFO"  # Default value

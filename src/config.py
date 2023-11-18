__all__ = ["Environment", "settings", "Settings"]

import os
from enum import StrEnum
from pathlib import Path
from typing import Optional

import yaml
from pydantic import SecretStr, model_validator, BaseModel, Field, ConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Smtp(BaseModel):
    SERVER: str = "mail.innopolis.ru"
    PORT: int = 587
    USERNAME: str
    PASSWORD: SecretStr

    @model_validator(mode="before")
    def all_keys_to_upper(cls, values):
        return {key.upper(): value for key, value in values.items()}


class Cookies(BaseModel):
    # Authentication
    NAME: str = "token"
    DOMAINS: str = "innohassle.ru"
    ALLOWED_DOMAINS: list[str] = ["innohassle.ru", "api.innohassle.ru", "localhost"]

    @model_validator(mode="before")
    def all_keys_to_upper(cls, values):
        return {key.upper(): value for key, value in values.items()}


class Settings(BaseModel):
    """
    Settings for the application. Get settings from .env file.
    """

    model_config = ConfigDict(extra="ignore")

    # Prefix for the API path (e.g. "/api/v0")
    APP_ROOT_PATH: str = ""
    # App environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    # PostgreSQL database connection URL
    DB_URL: SecretStr
    # Authentication
    COOKIE: Cookies = Field(default_factory=Cookies)
    # CORS configuration
    CORS_ALLOW_ORIGINS: list[str] = [
        "https://moperator.innohassle.ru",
        "http://localhost:3000",
    ]
    # JWT settings
    JWT_SECRET_KEY: str
    JWT_PUBLIC_KEY: str

    # SMTP server settings
    SMTP_ENABLED: bool = False
    SMTP: Optional[Smtp] = None

    def flatten(self):
        """
        Flatten settings to dict.
        """
        nested = self.model_dump(include={"SMTP", "COOKIE"})
        flattened = self.model_dump(exclude={"model_config", "SMTP", "COOKIE"})

        for key, value in nested.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    flattened[f"{key}__{k}"] = v
            else:
                flattened[key] = value

        return flattened

    @model_validator(mode="before")
    def all_keys_to_upper(cls, values):
        return {key.upper(): value for key, value in values.items()}

    @classmethod
    def from_yaml(cls, path: Path) -> "Settings":
        with open(path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        return cls.model_validate(yaml_config)


settings_path = os.getenv("SETTINGS_PATH")
if settings_path is None:
    settings_path = "settings.yaml"
settings = Settings.from_yaml(Path(settings_path))

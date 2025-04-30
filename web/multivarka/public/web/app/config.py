from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, field_validator, ValidationError
from typing import Optional
import os
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True 
    )

    POSTGRES_USER: str = Field(
        default="postgres",
        description="PostgreSQL username"
    )
    POSTGRES_PASSWORD: str = Field(
        default="postgres",
        description="PostgreSQL password"
    )
    POSTGRES_HOST: str = Field(
        default="localhost",
        description="PostgreSQL host"
    )
    POSTGRES_PORT: int = Field(
        default=5432,
        description="PostgreSQL port"
    )
    POSTGRES_DB: str = Field(
        default="postgres",
        description="PostgreSQL database name"
    )

    CLICKHOUSE_HOST: str = Field(
        default="localhost",
        description="ClickHouse server host"
    )
    CLICKHOUSE_PORT: int = Field(
        default=9000,
        description="ClickHouse server port"
    )
    CLICKHOUSE_DB: str = Field(
        default="default",
        description="ClickHouse database name"
    )
    CLICKHOUSE_USER: str = Field(
        default="default",
        description="ClickHouse username"
    )
    CLICKHOUSE_PASSWORD: str = Field(
        default="",
        description="ClickHouse password"
    )

    @property
    def pg_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def clickhouse_url(self) -> str:
        auth = f"{self.CLICKHOUSE_USER}:{self.CLICKHOUSE_PASSWORD}" if self.CLICKHOUSE_PASSWORD else self.CLICKHOUSE_USER
        return f"clickhouse://{auth}@{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}/{self.CLICKHOUSE_DB}"

    @field_validator('POSTGRES_HOST', 'CLICKHOUSE_HOST')
    def validate_hosts(cls, value: str) -> str:
        try:
            socket.gethostbyname(value)
            return value
        except socket.gaierror:
            raise ValueError(f"Could not resolve host: {value}")

    @field_validator('POSTGRES_PORT', 'CLICKHOUSE_PORT')
    def validate_ports(cls, value: int) -> int:
        """Validate port ranges"""
        if not 1 <= value <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return value

def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        logger.error("Configuration validation error: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected configuration error: %s", e)
        raise

settings = get_settings()


print("Current Settings:")
print(f"PostgreSQL URL: {settings.pg_url}")
print(f"ClickHouse URL: {settings.clickhouse_url}")
print("\nEnvironment variables used:")
for field in Settings.model_fields:
    print(f"{field}: {getattr(settings, field)}")
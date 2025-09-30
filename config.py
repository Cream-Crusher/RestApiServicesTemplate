from contextlib import suppress
from enum import StrEnum
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

with suppress(Exception):
    env_file = ".env"
    load_dotenv(dotenv_path=env_file)


class EnvironmentEnum(StrEnum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


class LogLevelEnum(StrEnum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class PosthogConfig(BaseSettings):
    host: str = "localhost"
    token: str | None = None

    class Config:
        env_prefix: str = "POSTHOG_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class BotConfig(BaseSettings):
    token: str
    subscribe_channel_url: str | None = None
    subscribe_channel_id: int | None = None
    web_app_url: str | None = None

    class Config:
        env_prefix: str = "BOT_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class DatabaseConfig(BaseSettings):
    port: int = 5432
    host: str
    database: str = Field(alias="POSTGRES_DATABASE")
    user: str
    password: str

    url: str = ""

    class Config:
        env_prefix: str = "POSTGRES_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)
        self.url = self._assemble_database_url()

    def _assemble_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseSettings):
    host: str | None = None

    class Config:
        env_prefix: str = "REDIS_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class MinioConfig(BaseSettings):
    access_key: str | None = Field(alias="S3_ACCESS", default=None)
    secret_key: str | None = Field(alias="S3_SECRET", default=None)
    endpoint: str | None = Field(alias="S3_ENDPOINT", default=None)

    class Config:
        env_prefix: str = "S3_"


class AppConfig(BaseSettings):
    environment: EnvironmentEnum = EnvironmentEnum.LOCAL
    log_level: LogLevelEnum = LogLevelEnum.DEBUG

    class Config:
        env_prefix: str = "APP_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class OAuth2(BaseSettings):
    token_url: str
    scheme_name: str
    algorithm: str
    key: str

    class Config:
        env_prefix: str = "OAuth2_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class AppSettings(BaseModel):
    bot_config: BotConfig = BotConfig()
    database_config: DatabaseConfig = DatabaseConfig()
    redis_config: RedisConfig = RedisConfig()
    posthog_config: PosthogConfig = PosthogConfig()
    minio_config: MinioConfig = MinioConfig()
    app_config: AppConfig = AppConfig()
    oauth2: OAuth2 = OAuth2()


settings = AppSettings()

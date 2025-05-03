from contextlib import suppress
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

with suppress(Exception):
    env_file = '.env'
    load_dotenv(dotenv_path=env_file)


class PosthogConfig(BaseSettings):
    token: str | None = None

    class Config:
        env_prefix: str = "POSTHOG_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class BotConfig(BaseSettings):
    token: str
    subscribe_channels: str | None = None

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
    disable: bool = True
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
    environment_type: Literal["local", "dev", "prod"] | str = "dev"
    log_level: str = "DEBUG"

    class Config:
        env_prefix: str = "APP_"

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)


class AppSettings(BaseModel):
    bot_config: BotConfig = BotConfig()
    database_config: DatabaseConfig = DatabaseConfig()
    redis_config: RedisConfig = RedisConfig()
    posthog_config: PosthogConfig = PosthogConfig()
    minio_config: MinioConfig = MinioConfig()
    app_config: AppConfig = AppConfig()


settings = AppSettings()

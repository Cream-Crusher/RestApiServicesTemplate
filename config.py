from contextlib import suppress

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

with suppress(Exception):
    env_file = 'deploy/env/.env'
    load_dotenv(env_file)


class PosthogConfig(BaseSettings):
    token: str | None = None

    class Config:
        env_prefix = "POSTHOG_"

    def __init__(self, **values):
        super().__init__(**values)


class BotConfig(BaseSettings):
    token: str
    subscribe_channels: str | None = None

    class Config:
        env_prefix = "BOT_"

    def __init__(self, **values):
        super().__init__(**values)


class DatabaseConfig(BaseSettings):
    port: int = 5432
    host: str
    database: str = Field(alias="POSTGRES_DATABASE")
    user: str
    password: str

    url: str = ""

    class Config:
        env_prefix = "POSTGRES_"

    def __init__(self, **values):
        super().__init__(**values)
        self.url = self._assemble_database_url()

    def _assemble_database_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseSettings):
    disable: bool = True
    host: str | None = None

    class Config:
        env_prefix = "REDIS_"

    def __init__(self, **values):
        super().__init__(**values)


class MinioConfig(BaseSettings):
    access_key: str | None = Field(alias="ACCESS", default=None)
    secret_key: str | None = Field(alias="SECRET", default=None)
    endpoint: str | None = Field(alias="ENDPOINT", default=None)

    class Config:
        env_prefix = "S3_"

    def __init__(self, **values):
        super().__init__(**values)


class ApiServiseConfig(BaseSettings):
    dev: bool = False


class AppSettings(BaseModel):
    bot_config: BotConfig = BotConfig()
    database_config: DatabaseConfig = DatabaseConfig()
    redis_config: RedisConfig = RedisConfig()
    posthog_config: PosthogConfig = PosthogConfig()
    minio_config: MinioConfig = MinioConfig()
    api_servise_config: ApiServiseConfig = ApiServiseConfig()


settings = AppSettings()

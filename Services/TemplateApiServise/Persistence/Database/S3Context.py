from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

import aioboto3
from loguru import logger
from types_aiobotocore_s3 import S3Client

from config import DatabaseConfig, config

Database: DatabaseConfig = config.database_config


class S3Context:
    def __init__(self, endpoint: str | None, access_key: str | None, secret_key: str | None) -> None:
        assert endpoint is not None
        assert access_key is not None
        assert secret_key is not None
        logger.info(f"\nendpoint: {endpoint}\naccess_key: {access_key},\nsecret_key: {secret_key}")

        self.endpoint: str = f"https://{endpoint}"
        self.access_key: str = access_key
        self.secret_key: str = secret_key
        self.session: aioboto3.Session = aioboto3.Session()

    @asynccontextmanager
    async def session_client(self) -> AsyncGenerator[S3Client, None]:
        async with cast(
            S3Client,
            self.session.client(
                service_name="s3",
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            ),
        ) as client:
            yield client


s3_context: S3Context = S3Context(
    endpoint=config.minio_config.endpoint,
    access_key=config.minio_config.access_key,
    secret_key=config.minio_config.secret_key,
)

from contextlib import asynccontextmanager
from contextlib import asynccontextmanager
from typing import cast, AsyncGenerator

import aioboto3
from types_aiobotocore_s3 import S3Client

from config import settings

Database = settings.database_config


class S3Context:
    def __init__(self, endpoint: str, access_key: str, secret_key: str):
        self.endpoint = f"https://{endpoint}"
        self.access_key = access_key
        self.secret_key = secret_key
        self.session = aioboto3.Session()

    @asynccontextmanager
    async def session_client(self) -> AsyncGenerator[S3Client, None]:
        async with cast(
            S3Client,
            self.session.client(
                "s3",
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            ),
        ) as client:
            yield client


s3_context: S3Context = S3Context(
    endpoint=settings.minio_config.endpoint,
    access_key=settings.minio_config.access_key,
    secret_key=settings.minio_config.secret_key,
)

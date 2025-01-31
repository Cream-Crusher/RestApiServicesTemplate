import logging
from typing import cast

import aioboto3
from types_aiobotocore_s3 import S3Client

from Services.TemplateApiServise.WebApi.config import settings

Database = settings.database_config


class S3Context:
    def __init__(self, endpoint: str, access_key: str, secret_key: str):
        self.endpoint = "https://"+endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.session = aioboto3.Session()
        self.client = self.session.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    async def get_session(self) -> S3Client:
        async with cast(S3Client, self.client) as client:
            try:
                yield client
            except Exception as error:
                logging.error(error)
                await client.close()
                raise


s3_context: S3Context = S3Context(
    endpoint=settings.minio_config.endpoint,
    access_key=settings.minio_setting.access,
    secret_key=settings.minio_setting.secret,
)

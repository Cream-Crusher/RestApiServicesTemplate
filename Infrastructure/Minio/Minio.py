import logging
from contextlib import asynccontextmanager
from io import BytesIO
from typing import cast, AsyncGenerator

import aioboto3
from types_aiobotocore_s3 import S3Client

from Services.TemplateApiServise.WebApi.config import settings


class MinioUploader:
    def __init__(self, endpoint: str, access_key: str, secret_key: str):
        self.endpoint = "https://"+endpoint
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

    async def is_exists_bucket(self, bucket: str) -> bool:
        async with cast(S3Client, self.session_client()) as s3_client:
            response = await s3_client.list_buckets()

        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        return bucket in buckets

    async def create_bucket_if_not_exists(self, bucket: str) -> None:
        if not await self.is_exists_bucket(bucket):
            async with cast(S3Client, self.session_client()) as s3_client:
                await s3_client.create_bucket(Bucket=bucket)

    def compare_link(self, bucket_name: str, object_name: str) -> str:
        return f"{self.endpoint}/{bucket_name}/{object_name}"

    async def upload_file_obj(
        self, bucket_name: str, body: BytesIO, object_name: str, content_type: str
    ) -> str:
        # Использование клиента s3
        body.seek(0)

        async with cast(S3Client, self.session_client()) as s3_client:
            try:
                await self.create_bucket_if_not_exists(bucket_name)
                # Загрузка файла в Minio
                await s3_client.upload_fileobj(
                    body,
                    bucket_name,
                    object_name,
                    ExtraArgs={
                        # 'x-amz-acl': 'public-read',
                        "ContentType": content_type,
                        "ACL": "public-read",
                    },
                )  # type: ignore
                logging.info(
                    f"Файл '{object_name}' успешно загружен в бакет '{bucket_name}'"
                )
            except Exception as e:
                logging.exception(f"Произошла ошибка при загрузке файла: {e}")

        return self.compare_link(bucket_name, object_name)

    async def get_file(self, bucket_name: str, object_name: str) -> BytesIO:

        async with cast(S3Client, self.session_client()) as s3_client:
            file = await s3_client.get_object(Bucket=bucket_name, Key=object_name)
            body = BytesIO(await file["Body"].read())

        body.name = object_name
        return body


s3_manager: MinioUploader = MinioUploader(
    endpoint=settings.minio_setting.endpoint,
    access_key=settings.minio_setting.access,
    secret_key=settings.minio_setting.secret,
)

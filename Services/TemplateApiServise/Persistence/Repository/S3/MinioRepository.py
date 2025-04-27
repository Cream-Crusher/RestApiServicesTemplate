from io import BytesIO
from typing import cast, Any

from loguru import logger
from types_aiobotocore_s3 import S3Client

from Services.TemplateApiServise.Persistence.Database.S3Context import s3_context, S3Context
from Services.TemplateApiServise.Persistence.Repository.S3.BaseS3Repository import BaseS3Repository


class MinioRepository(BaseS3Repository[BytesIO]):
    def __init__(self, s3_context: S3Context) -> None:
        self.endpoint: str = f"https://{s3_context.endpoint}" if 'https://' not in s3_context.endpoint else s3_context.endpoint
        self.s3_context: S3Context = s3_context

    async def _is_exists_bucket(self, bucket: str) -> bool:
        async with self.s3_context.session_client() as s3_client:
            response: Any = await s3_client.list_buckets()

        buckets: list[str] = [bucket["Name"] for bucket in response["Buckets"]]
        return bucket in buckets

    async def _create_bucket_if_not_exists(self, bucket: str) -> None:
        if not await self._is_exists_bucket(bucket=bucket):
            async with cast(S3Client, self.s3_context.session_client()) as s3_client:
                await s3_client.create_bucket(Bucket=bucket)

    def _compare_link(self, bucket_name: str, object_name: str) -> str:
        return f"{self.endpoint}/{bucket_name}/{object_name}"

    async def upload(self, body: BytesIO, object_name: str, bucket_name: str, content_type: str) -> str:
        body.seek(0)
        async with cast(S3Client, self.s3_context.session_client()) as s3_client:
            try:
                await self._create_bucket_if_not_exists(bucket=bucket_name)
                await s3_client.upload_fileobj(
                    Fileobj=body,
                    Bucket=bucket_name,
                    Key=object_name,
                    ExtraArgs={
                        # 'x-amz-acl': 'public-read',
                        "ContentType": content_type,
                        "ACL": "public-read",
                    },
                )  # type: ignore
                logger.info(
                    f"Файл '{object_name}' успешно загружен в бакет '{bucket_name}'"
                )
            except Exception as e:
                logger.exception(f"Произошла ошибка при загрузке файла: {e}")

        return self._compare_link(bucket_name=bucket_name, object_name=object_name)

    async def get(self, object_name: str, bucket_name: str) -> BytesIO:
        async with cast(S3Client, self.s3_context.session_client()) as s3_client:
            file = await s3_client.get_object(Bucket=bucket_name, Key=object_name)
            body = BytesIO(initial_bytes=await file["Body"].read())

        body.name = object_name
        return body

    async def remove(self, object_name: str, bucket_name: str) -> None:
        pass
        # await self.session.delete_object(Bucket=bucket_name, Key=object_name)

    async def update(self, body: BytesIO, object_name: str, bucket_name: str, content_type: str) -> str:
        await self.remove(object_name=object_name, bucket_name=bucket_name)
        return await self.upload(body=body, object_name=object_name, bucket_name=bucket_name, content_type=content_type)


s3_manager: MinioRepository = MinioRepository(
    s3_context=s3_context
)
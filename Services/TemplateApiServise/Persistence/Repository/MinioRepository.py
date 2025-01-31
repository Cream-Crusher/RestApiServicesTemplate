import logging
from io import BytesIO

from types_aiobotocore_s3 import S3Client

from Services.TemplateApiServise.Persistence.Database.S3Context import s3_context
from Services.TemplateApiServise.Persistence.Repository.BaseS3Repository import BaseS3Repository
from Services.TemplateApiServise.WebApi.config import settings


class MinioRepository[T1, T2](BaseS3Repository):
    def __init__(self, endpoint: str, session: S3Client):
        self.endpoint = "https://"+endpoint
        self.session = session

    async def _is_exists_bucket(self, bucket: str) -> bool:
        response = await self.session.list_buckets()

        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        return bucket in buckets

    async def _create_bucket_if_not_exists(self, bucket: str) -> None:
        if not await self._is_exists_bucket(bucket):
            await self.session.create_bucket(Bucket=bucket)

    def _compare_link(self, bucket_name: str, object_name: str) -> str:
        return f"{self.endpoint}/{bucket_name}/{object_name}"

    async def upload(self, body: T1, object_name: T2, bucket_name: T2, content_type: T2) -> T2:
        body.seek(0)

        try:
            await self._create_bucket_if_not_exists(bucket_name)
            # Загрузка файла в Minio
            await self.session.upload_fileobj(
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

        return self._compare_link(bucket_name, object_name)

    async def get(self, object_name: T2, bucket_name: T2) -> T1:
        file = await self.session.get_object(Bucket=bucket_name, Key=object_name)
        body = BytesIO(await file["Body"].read())

        return body

    async def remove(self, object_name: T2, bucket_name: T2) -> None:
        await self.session.delete_object(Bucket=bucket_name, Key=object_name)

    async def update(self, body: T1, object_name: T2, bucket_name: T2, content_type: T2) -> T2:
        await self.remove(object_name, bucket_name)
        return await self.upload(body, object_name, bucket_name, content_type)


s3_manager: MinioRepository = MinioRepository[BytesIO, str](
    endpoint=settings.minio_setting.endpoint,
    session=s3_context.get_session()  # todo костыль до добавления di
)

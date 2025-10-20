from io import BytesIO

from Services.TemplateApiServise.Persistence.Repository.S3.MinioRepository import s3_manager


class S3Repository:
    """Репозиторий для работы с S3 хранилищем"""

    def __init__(self, bucket_name: str = "general"):
        self.bucket_name = bucket_name

    async def upload_file(self, file_data: bytes, object_name: str, content_type: str = "image/jpeg") -> str:
        """Загрузить файл в S3"""
        file_obj = BytesIO(file_data)
        return await s3_manager.upload(
            body=file_obj,
            object_name=object_name,
            bucket_name=self.bucket_name,
            content_type=content_type
        )

    async def get_file(self, object_name: str) -> BytesIO:
        """Получить файл из S3"""
        return await s3_manager.get(
            object_name=object_name,
            bucket_name=self.bucket_name
        )

    def get_file_url(self, object_name: str) -> str:
        """Получить URL файла в S3"""
        return f"{s3_manager.endpoint}/{self.bucket_name}/{object_name}"


# Создаем экземпляр репозитория
s3_repository = S3Repository()

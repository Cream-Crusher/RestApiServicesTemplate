from typing import Protocol


class BaseS3Repository[T](Protocol):

    async def upload(self, body: T, object_name: str, bucket_name: str, content_type: str) -> str: ...

    async def get(self, object_name: str, bucket_name: str) -> T: ...

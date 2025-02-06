from typing import Protocol


class BaseS3Repository[T1, T2, T3](Protocol):

    async def upload(self, body: T1, object_name: T2, bucket_name: T2, content_type: T2) -> T2:
        ...

    async def get(self, object_name: T2, bucket_name: T3) -> T1:
        ...

    async def remove(self, object_name: T2, bucket_name: T2) -> None:
        ...

    async def update(self, body: T1, object_name: T2, bucket_name: T2, content_type: T2) -> T2:
        ...

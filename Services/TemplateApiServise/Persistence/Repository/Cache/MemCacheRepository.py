import time
from typing import Iterable, Union

from Services.TemplateApiServise.Persistence.Repository.Cache.BaseCacheRepository import BaseCacheRepository


class MemCacheRepository(BaseCacheRepository):
    def __init__(self) -> None:
        self.kv = {}

    async def get(self, key: str):
        if key not in self.kv:
            return None
        value, ttl = self.kv[key]
        if ttl is not None and ttl < time.monotonic():
            return None
        return value

    async def expire(self, key: str, ex: float):
        self.kv[key] = self.kv[key][0], ex + time.monotonic()

    async def set(self, key: str, value, ex: float | None = None):
        self.kv[key] = value, ex and ex + time.monotonic()

    async def lpush(self, key: str, *values: bytes):
        self.kv.setdefault(key, []).extend(values)

    async def lrem(self, key: str, count: int, value: bytes):
        assert count == 1
        self.kv.setdefault(key, []).remove(value)
        return count

    async def lrange(self, key: str, start: int, end: int) -> list[bytes]:
        return self.kv.setdefault(key, [])[start:end]

    async def mget(self, keys: Iterable[str]):
        return [await self.get(key) for key in keys]

    async def incr(self, key: str):
        value = await self.get(key) or 0
        value += 1
        await self.set(key, value)
        return value

    async def zincrby(self, key: str, value: float, item: str):
        data = self.kv.setdefault(key, {})
        data.setdefault(item, 0)
        data[item] += value
        self.kv[key] = {k: v for k, v in sorted(data.items(), key=lambda x: x[1])}

    async def zrevrange(
        self, key: str, start: int, end: int
    ) -> list[tuple[bytes, float]]:
        return list(self.kv.setdefault(key, {}).items())[::-1][start: end + 1]

    async def zrange(
        self, key: str, start: int, end: int
    ) -> list[tuple[bytes, float]]:
        return list(self.kv.setdefault(key, {}).items())[start: end + 1]

    async def zscore(self, key: str, name: str):
        return self.kv.setdefault(key, {}).get(name)

    async def zrem(self, key: str, name: str):
        return self.kv.setdefault(key, {}).pop(name)

    async def zadd(self, key: str, data: dict):
        self.kv.setdefault(key, {}).update(data)

    async def zrevrank(self, key: str, item: str) -> Union[None, int]:
        result = [
            x
            for x, v in enumerate(list(self.kv.setdefault(key, {}))[::-1])
            if v == item
        ]
        if result:
            return result[0]

        return None


MemCacheRepositoryInstance: MemCacheRepository = MemCacheRepository()

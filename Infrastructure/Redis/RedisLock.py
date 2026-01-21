import asyncio
import uuid
from typing import Any

from redis.asyncio import Redis


class RedisLock:
    def __init__(self, redis_client: Redis, lock_key: str, expire: int = 10, timeout: int = 5):
        self.redis_client = redis_client
        self.lock_key = lock_key
        self.expire = expire
        self.timeout = timeout
        self.token = str(uuid.uuid4())

    async def __aenter__(self):
        return await self.acquire()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        await self.release()

    async def acquire(self) -> bool:
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < self.timeout:
            if await self.redis_client.set(self.lock_key, self.token, nx=True, ex=self.expire):
                return True
            await asyncio.sleep(0.1)
        return False

    async def release(self):
        # Only release the lock if we are the ones who hold it
        if await self.redis_client.get(self.lock_key) == self.token:
            await self.redis_client.delete(self.lock_key)


# Пример
# async with RedisLock(self.redis_client, self.lock_key) as acquired:
#     if not acquired:
#         logger.info("Another QR worker instance is running, skipping...")
#         return

from redis.asyncio import Redis

from Infrastructure.Redis.Client import async_redis_client
from Services.TemplateApiServise.Application.common.exceptions.RateLimitError import RateLimitError


class RateLimit:
    def __init__(self, redis_client: Redis, max_calls: int, period_seconds: int):
        self.redis_client = redis_client
        self.max_calls = max_calls
        self.period = period_seconds

    async def acquire(self, key: str = "all"):
        counter = await self.redis_client.incr(key)
        if counter == 1:
            await self.redis_client.expire(key, self.period)
        if counter > self.max_calls:
            raise RateLimitError(key, self.max_calls, self.period)


ip_limiter = RateLimit(async_redis_client, 2, 10)
# Пример использования: await ip_limiter.acquire(x_forwarded_for)

from Services.TemplateApiServise.Application.exceptions.RateLimitError import RateLimitError
from Services.TemplateApiServise.Persistence.Repository.Cache.CacheInstanceRepository import cache_repository_instance
from Services.TemplateApiServise.Persistence.Repository.Cache.MemCacheRepository import MemCacheRepository
from Services.TemplateApiServise.Persistence.Repository.Cache.RedisCacheRepository import RedisCacheRepository


class RateLimit:
    def __init__(self, cache: MemCacheRepository | RedisCacheRepository, max_calls: int, period_seconds: int):
        self.cache = cache
        self.max_calls = max_calls
        self.period = period_seconds

    async def acquire(self, key: str = "all"):
        counter = await self.cache.incr(key)
        if counter == 1:
            await self.cache.expire(key, self.period)
        if counter > self.max_calls:
            raise RateLimitError(key, self.max_calls, self.period)


ip_limiter = RateLimit(cache_repository_instance, 2, 10)
# Пример использования: await ip_limiter.acquire(x_forwarded_for)

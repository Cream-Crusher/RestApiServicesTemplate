from functools import cache
from typing import Literal

from config import settings
from Services.TemplateApiServise.Persistence.Repository.Cache.MemCacheRepository import (
    MemCacheRepository,
)
from Services.TemplateApiServise.Persistence.Repository.Cache.RedisCacheRepository import (
    RedisCacheRepository,
)


@cache
def connect_cache_repository_instance(
    cache_type: Literal["redis", "memory"], host: str | None = None
) -> MemCacheRepository | RedisCacheRepository:

    match cache_type:
        case "redis":
            assert host is not None, "cache_type is redis, but host is None"
            return RedisCacheRepository(host=host)
        case "memory":
            return MemCacheRepository()
        case _:
            return MemCacheRepository()


cache_repository_instance: MemCacheRepository | RedisCacheRepository = connect_cache_repository_instance(
    "redis", settings.redis_config.host
)

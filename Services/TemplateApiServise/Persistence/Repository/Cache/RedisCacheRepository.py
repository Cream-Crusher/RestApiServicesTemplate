from Services.TemplateApiServise.Persistence.Repository.Cache.BaseCacheRepository import BaseCacheRepository
from config import RedisConfig, settings
from redis.asyncio import Redis


class RedisCacheRepository(BaseCacheRepository, Redis):  # type: ignore
    def __init__(self, config: RedisConfig) -> None:
        self.redis = Redis(
            host=config.host or "localhost",
            decode_responses=True
        )


RedisCacheRepositoryInstance: RedisCacheRepository = RedisCacheRepository(config=settings.redis_config)  # type: ignore

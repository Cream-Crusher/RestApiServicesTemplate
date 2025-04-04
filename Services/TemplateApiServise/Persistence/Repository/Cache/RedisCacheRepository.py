from Services.TemplateApiServise.Persistence.Repository.Cache.BaseCacheRepository import BaseCacheRepository
from config import RedisConfig, settings
from redis.asyncio import Redis


class RedisCacheRepository(BaseCacheRepository, Redis):

    def __init__(self, config: RedisConfig):
        super().__init__(
            host=config.host,
            decode_responses=True
        )


RedisCacheRepositoryInstance: RedisCacheRepository = RedisCacheRepository(settings.redis_config)

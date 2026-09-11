from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from config import config


redis_client = Redis(host=config.redis_config.host)
async_redis_client = AsyncRedis(host=config.redis_config.host, decode_responses=True)

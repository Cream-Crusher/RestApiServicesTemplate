import json
from typing import Any, Callable

from pydantic import BaseModel

from Services.TemplateApiServise.Persistence.Repository.Cache.CacheInstanceRepository import CacheRepositoryInstance
from Services.TemplateApiServise.Persistence.Repository.Cache.RedisCacheRepository import RedisCacheRepository


class ModelCacheService:
    
    def __init__(
            self,
            cache: RedisCacheRepository
    ):
        self.cache = cache
    
    async def get[T](self, key: str, callback: Callable[..., T]) -> T | None:
        cached_user = await self.cache.get(key)

        if cached_user:
            return callback(**json.loads(cached_user))
        
        return None
    
    async def set(self, key: str, model: BaseModel, **kw: Any):
        await self.cache.set(name=key, value=json.dumps(model.model_dump()), ex=300, **kw)
    
    async def delete(self, key: str):
        await self.cache.delete(key)


model_cache_service = ModelCacheService(
    cache=CacheRepositoryInstance  # type: ignore
)
import json
from collections.abc import Callable
from contextlib import suppress
from typing import Any

from pydantic import BaseModel
from redis.exceptions import ConnectionError

from Services.TemplateApiServise.Persistence.Repository.Cache.CacheInstanceRepository import (
    CacheRepositoryInstance,
)
from Services.TemplateApiServise.Persistence.Repository.Cache.RedisCacheRepository import (
    RedisCacheRepository,
)


class ModelCacheService:

    def __init__(self, cache: RedisCacheRepository):
        self.cache = cache

    async def get[T](self, key: str, callback: Callable[..., T]) -> T | None:  # type: ignore
        """
        get cache model by key

        :param key: key of model
        :param callback: pydantic model

        :return: pydantic model or None
        """

        with suppress(ConnectionError):
            cached_model = await self.cache.get(key)

            if cached_model:
                return callback(**json.loads(cached_model))

            return None

    async def set(self, key: str, model: BaseModel, **kw: Any):
        """
        set cache model by key

        :param key: key of model
        :param model: pydantic model
        :param kw: Any redis.set parameter

        :return: pydantic model or None
        """

        with suppress(ConnectionError):
            await self.cache.set(name=key, value=json.dumps(model.model_dump()), ex=300, **kw)

    async def delete(self, key: str):
        """
        delete cache model by key

        :param key: key of model
        """
        with suppress(ConnectionError):
            await self.cache.delete(key)


model_cache_service = ModelCacheService(cache=CacheRepositoryInstance)  # type: ignore

import json
from collections.abc import Callable, Iterable
from contextlib import suppress
from datetime import datetime
from typing import Any, get_args, get_origin, overload
from uuid import UUID

from pydantic import BaseModel, ValidationError
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

    @staticmethod
    def _default_serializer(obj: Any) -> str:
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()

        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    async def get[T](self, key: str, callback: Callable[..., T]) -> T | None:  # type: ignore
        """
        get cache model by key

        :param key: key of model
        :param callback: pydantic model | list[model]

        :return: pydantic model or list[model] or None
        """
        with suppress(ConnectionError, ValidationError):
            cached_model = await self.cache.get(key)

            if cached_model is None:
                return None
            elif get_origin(callback) is list:
                item_type = get_args(callback)[0]
                return [item_type(**item) for item in json.loads(cached_model)]  # type: ignore
            elif cached_model:
                return callback(**json.loads(cached_model))

        return None

    @overload
    async def set(self, key: str, models: Iterable[BaseModel], ex: int = 300, **kw: Any) -> None: ...

    @overload
    async def set(self, key: str, models: BaseModel, ex: int = 300, **kw: Any) -> None: ...

    async def set(self, key: str, models: BaseModel | Iterable[BaseModel], ex: int = 300, **kw: Any) -> None:
        """
        set cache model by key

        :param key: key of model
        :param models: pydantic models or model
        :param ex: ex time
        :param kw: Any redis.set parameter
        """
        with suppress(ConnectionError):
            if isinstance(models, BaseModel):
                await self.cache.set(name=key, value=json.dumps(models.model_dump(mode="json")), ex=ex, **kw)
            elif models:
                await self.cache.set(
                    name=key,
                    value=json.dumps([model.model_dump(mode="json") for model in models]),
                    ex=ex,
                    **kw,
                )

    @overload
    async def delete(self, keys: str) -> None: ...  # type: ignore

    @overload
    async def delete(self, keys: Iterable[str]) -> None: ...  # type: ignore

    async def delete(self, keys: Iterable[str] | str):
        """
        delete cache model by key

        :param keys: key of model
        """
        with suppress(ConnectionError):
            if isinstance(keys, str):
                await self.cache.delete(keys)
            else:
                for key in keys:
                    await self.cache.delete(key)


model_cache_service = ModelCacheService(cache=CacheRepositoryInstance)  # type: ignore

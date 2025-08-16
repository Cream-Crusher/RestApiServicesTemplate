from typing import Callable

from Services.TemplateApiServise.Application.common.ModelCacheService import (
    ModelCacheService,
    model_cache_service,
)
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound


class BaseQueryService[T, I]:

    def __init__(
        self,
        model: type[T],
        cache_service: ModelCacheService = model_cache_service,
    ) -> None:
        self.model: type[T] = model
        self.cache_service = cache_service

    async def get_by_id(self, model_id: int, callback_dto: Callable[..., T]) -> T | None:  # type: ignore
        cached_key = f"{self.model.__class__.__name__}:{model_id}"
        cached_model = await self.cache_service.get(key=cached_key, callback=callback_dto)

        if cached_model:
            return cached_model

        real_model: T = await self.model.select().where(self.model.id == model_id).one_or_raise(ModelNotFound(self.model))
        return_real_model = callback_dto(**real_model.__dict__)
        await self.cache_service.set(cached_key, return_real_model)

        return return_real_model

    async def get_all[TM](self, callback: Callable[[T], TM]) -> TM:
        pass

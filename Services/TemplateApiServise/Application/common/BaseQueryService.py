from collections.abc import Callable

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

    async def set_and_return[TM](self, cached_key: str, real_model: T, callback_dto: Callable[..., TM]) -> TM:
        return_real_model = callback_dto.model_validate(real_model, from_attributes=True)
        await self.cache_service.set(cached_key, return_real_model)

        return return_real_model

    async def get_by_id[TM](self, model_id: int, callback_dto: Callable[..., TM]) -> TM | None:  # type: ignore
        cached_key = f"{self.model.__tablename__}:{model_id}"
        cached_model = await self.cache_service.get(key=cached_key, callback=callback_dto)

        if cached_model:
            return cached_model

        real_model: T = (
            await self.model.select().where(self.model.id == model_id).one_or_raise(ModelNotFound(self.model))
        )
        return await self.set_and_return(cached_key, real_model, callback_dto)

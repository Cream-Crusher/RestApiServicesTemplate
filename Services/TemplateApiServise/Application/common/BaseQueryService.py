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

    async def set_and_return[TM](self, cached_key: str, model: T, callback_dto: Callable[..., TM]) -> TM:
        model_dto = callback_dto.model_validate(model, from_attributes=True)
        await self.cache_service.set(cached_key, model_dto)

        return model_dto

    async def get_by_id[TM](self, model_id: I, callback_dto: Callable[..., TM]) -> TM | None:  # type: ignore
        cached_key = f"{self.model.__tablename__}:{model_id}"
        cached_model = await self.cache_service.get(key=cached_key, callback=callback_dto)

        if cached_model:
            return cached_model

        model: T = await self.model.select().where(self.model.id == model_id).one_or_raise(ModelNotFound(self.model))
        return await self.set_and_return(cached_key, model, callback_dto)

    async def get_all[TM](self, callback_dto: Callable[..., TM]) -> list[TM] | None:  # type: ignore
        cached_key = f"{self.model.__tablename__}:all"
        cached_model = await self.cache_service.get(key=cached_key, callback=list[callback_dto])

        if cached_model:
            return cached_model

        models_dto: T = (
            await self.model.select()
            .where(self.model.active.is_(True))
            .all_map(lambda model: callback_dto.model_validate(model, from_attributes=True))
        )
        await self.cache_service.set(cached_key, models_dto)
        return models_dto

from collections.abc import Iterable

from pydantic import BaseModel
from sqlalchemy import delete, update

from Services.TemplateApiServise.Application.common.ModelCacheService import (
    ModelCacheService,
    model_cache_service,
)
from Services.TemplateApiServise.Application.common.utcnow import utcnow
from Services.TemplateApiServise.Persistence.Database.DbContext import get_session


class BaseCommandService[T, I]:

    def __init__(
        self,
        model: type[T],
        cache_service: ModelCacheService = model_cache_service,
    ) -> None:
        self.model: type[T] = model
        self.cache_service = cache_service

    async def create(self, new_model: BaseModel | dict, keys: Iterable[str] | str | None = None):
        if isinstance(new_model, dict):
            self.model(**new_model).add()  # type: ignore
        else:
            self.model(**new_model.model_dump()).add()  # type: ignore

        if keys:
            await self.cache_service.delete(keys=keys)

    async def update(
        self, model_id: I, update_model: BaseModel | dict, keys: Iterable[str] | str | None = None
    ) -> None:
        if isinstance(update_model, dict):
            update_data = {**update_model, "updated_at": utcnow()}
        else:
            update_data = {**update_model.model_dump(exclude_none=True, exclude_unset=True), "updated_at": utcnow()}

        query = update(self.model).where(self.model.id == model_id).values(**update_data)  # type: ignore
        await get_session().execute(query)
        if keys:
            await self.cache_service.delete(keys=keys)
        await self.cache_service.delete(keys=f"{self.model.__tablename__}:{model_id}")

    async def delete(self, model_id: I, keys: Iterable[str] | str | None = None) -> None:
        query = delete(self.model).where(self.model.id == model_id)  # type: ignore
        await get_session().execute(query)
        if keys:
            await self.cache_service.delete(keys=keys)
        await self.cache_service.delete(keys=f"{self.model.__tablename__}:{model_id}")

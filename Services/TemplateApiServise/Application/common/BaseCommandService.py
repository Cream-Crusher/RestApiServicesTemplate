from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import delete, update

from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService, model_cache_service
from Services.TemplateApiServise.Persistence.Database.DbContext import get_session


class BaseCommandService[T, I]:

    def __init__(
            self,
            model: type[T],
            cache_service: ModelCacheService = model_cache_service,
    ) -> None:
        self.model: type[T] = model
        self.cache_service = cache_service

    def create(self, new_model: BaseModel) -> T:
        return self.model(**new_model.model_dump()).add()  # type: ignore

    async def update(self, model_id: I, update_model: BaseModel, cache_key: str | None = None) -> None:
        update_data = {**update_model.model_dump(), "updated_at": datetime.now()}
        query = update(self.model).where(self.model.id == model_id).values(**update_data)  # type: ignore
        await get_session().execute(query)
        if cache_key:
            await self.cache_service.delete(key=cache_key)

    async def delete(self, model_id: I, cache_key: str | None = None) -> None:
        query = delete(self.model).where(self.model.id == model_id)  # type: ignore
        await get_session().execute(query)
        if cache_key:
            await self.cache_service.delete(key=cache_key)

from datetime import datetime
from typing import Sequence, Any, Union

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from Services.TemplateApiServise.Application.common.Pagination import Pagination
from Services.TemplateApiServise.Persistence.Database.DbContext import get_session


class BaseService[T, I]:

    def __init__(self, model: type[T]) -> None:
        self.model: type[T] = model

    async def all(self, paging: None | Pagination = None) -> Sequence[T]:
        if paging is None:
            result: Any = (
                self.model.select()  # type: ignore
                .where(self.model.active.is_(True))  # type: ignore
            )
        else:
            result = await (
                self.model.select()  # type: ignore
                .where(self.model.active.is_(True))  # type: ignore
                .offset(paging.skip)
                .limit(paging.limit)
            )

        if not result:
            return []

        return result.all()

    async def id(self, model_id: I) -> T:
        return (
            await self.model.select()  # type: ignore
            .where(self.model.id == model_id)  # type: ignore
            .one_or_raise(HTTPException(status_code=404, detail=f'{self.model.__name__} {model_id} not found'))
        )  # type: ignore

    async def create(self, data: dict[str, Any]) -> T:
        return self.model(**data).add()  # type: ignore

    async def update(self, model_id: Union[T, I], update_data: dict[str, Any]) -> T:
        model: T = model_id if isinstance(type(model_id), type(I)) else await self.id(model_id=model_id)  # type: ignore

        for key, value in update_data.items():
            if value is not None:
                setattr(model, key, value)  # type: ignore

        model.updated_at = datetime.now(tz=None)  # type: ignore
        return model  # type: ignore

    async def delete(self, model_id: Union[T, I]) -> None:
        id_value: I = model_id if isinstance(model_id, I) else model_id.id  # type: ignore
        query = (
            delete(self.model)
            .where(self.model.id == id_value)  # type: ignore
        )
        session: AsyncSession = get_session()
        await session.execute(query)

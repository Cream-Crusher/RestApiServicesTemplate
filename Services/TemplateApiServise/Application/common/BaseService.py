from typing import Sequence, Any, Union
from uuid import UUID

from fastapi import HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from Services.TemplateApiServise.Application.common.Pagination import Pagination
from Services.TemplateApiServise.Application.common.utcnow import utcnow
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction, require_session


class BaseService[T, I]:

    def __init__(self, model: type[T]) -> None:
        self.model: type[T] = model

    async def all(self, paging: None | Pagination = None) -> Sequence[T]:
        if paging is None:
            query = (  # type: ignore
                self.model.select()  # type: ignore
                .where(self.model.active.is_(True))  # type: ignore
            )
        else:
            query = await (  # type: ignore
                self.model.select()  # type: ignore
                .where(self.model.active.is_(True))  # type: ignore
                .offset(paging.skip)
                .limit(paging.limit)
            )

        result = await query.all()  # type: ignore

        if not result:
            return []

        return result  # type: ignore

    async def id(self, model_id: I) -> T:
        return (
            await self.model.select()  # type: ignore
            .where(self.model.id == model_id)  # type: ignore
            .one_or_raise(HTTPException(status_code=404, detail=f'{self.model.__name__} {model_id} not found'))
        )  # type: ignore

    async def create(self, data: dict[str, Any]) -> T:
        try:
            user: T = self.model(**data).add()  # type: ignore
            return user  # type: ignore
        except IntegrityError as error:
            logger.error(error)
            raise error

    async def update(self, model_id: Union[str, int, T, UUID], update_data: dict[str, Any]) -> T:
        model: T = await self.id(model_id=model_id) if isinstance(model_id, Union[str, int, UUID]) else model_id  # type: ignore

        for key, value in update_data.items():
            if value is not None:
                setattr(model, key, value)

        model.updated_at = utcnow()  # type: ignore
        return model

    async def delete(self, model_id: Union[str, int, T, UUID]) -> None:
        model: T = await self.id(model_id=model_id) if isinstance(model_id, Union[str, int, UUID]) else model_id  # type: ignore

        session: AsyncSession = require_session()
        await session.delete(model)

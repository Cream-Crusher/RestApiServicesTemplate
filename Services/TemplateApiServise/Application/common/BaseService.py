from datetime import datetime, timezone
from typing import Sequence, Any, Tuple
from loguru import logger
from fastapi import HTTPException
from sqlalchemy import Row, RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from Services.TemplateApiServise.Persistence.Database.DbContext import transaction, require_session
from Services.TemplateApiServise.Application.common.Pagination import Pagination


class BaseService[T, I]:

    def __init__(self, model: type[T]) -> None:
        self.model: type[T] = model

    @transaction()  # type: ignore
    async def all(self, paging: None | Pagination = None) -> Sequence[Row[Tuple[T]] | RowMapping | Any]:
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

    @transaction()  # type: ignore
    async def id(self, model_id: I) -> T:
        return (
            await self.model.select()  # type: ignore
            .where(self.model.id == model_id)  # type: ignore
            .one_or_raise(HTTPException(status_code=404, detail=f'{self.model.__name__} {model_id} not found'))
        )  # type: ignore

    @transaction()  # type: ignore
    async def create(self, data: dict[str, Any]) -> T:
        try:
            user: T = self.model(**data).add()  # type: ignore
            session: AsyncSession = require_session()
            await session.commit()
            return user  # type: ignore
        except IntegrityError as error:
            logger.error(error)
            raise error

    @transaction()  # type: ignore
    async def update(self, model_id: str | T, update_data: dict[str, Any]) -> T:
        model: T = await self.id(model_id=model_id) if isinstance(model_id, str) else model_id  # type: ignore

        for key, value in update_data.items():
            if value is not None:
                setattr(model, key, value)

        model.updated_at = datetime.now(tz=timezone.utc)  # type: ignore
        session: AsyncSession = require_session()
        await session.commit()
        return model

    @transaction()  # type: ignore
    async def delete(self, model_id: str | T) -> None:
        model: T = await self.id(model_id=model_id) if isinstance(model_id, str) else model_id  # type: ignore

        session: AsyncSession = require_session()
        await session.delete(model)
        await session.commit()

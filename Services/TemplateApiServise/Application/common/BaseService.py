from datetime import datetime
from typing import Sequence, Any
from loguru import logger
from fastapi import HTTPException
from sqlalchemy import Row, RowMapping
from sqlalchemy.exc import IntegrityError

from Services.TemplateApiServise.Persistence.Database.DbContext import transaction, require_session


class BaseService[T, I]:

    def __init__(self, model: type[T]):
        self.model = model

    @transaction()
    async def all(self, paging=None) -> Sequence[Row | RowMapping | Any]:
        if paging is None:
            result = await (
                self.model.select()
                .where(self.model.active.is_(True))
            )
        else:
            result = await (
                self.model.select()
                .where(self.model.active.is_(True))
                .offset(paging.skip)
                .limit(paging.limit)
            )

        if not result:
            return []

        return result.all()

    @transaction()
    async def id(self, model_id: I) -> T:
        return (
            await self.model.select()
            .where(self.model.id == model_id)
            .one_or_raise(HTTPException(404, 'User not found'))
        )

    @transaction()
    async def create(self, data: dict) -> T:
        try:
            user = self.model(**data).add()
            session = require_session()
            await session.commit()
            return user
        except IntegrityError as error:
            logger.error(error)
            raise error

    @transaction()
    async def update(self, model_id: [str | T], update_data: dict) -> T:
        model = await self.id(model_id) if isinstance(model_id, str) else model_id

        for key, value in update_data.items():
            if value is not None:
                setattr(model, key, value)

        model.updated_at = datetime.utcnow()
        session = require_session()
        await session.commit()
        return model

    @transaction()
    async def delete(self, model_id: [str | T]):
        model = await self.id(model_id) if isinstance(model_id, str) else model_id

        session = require_session()
        await session.delete(model)
        await session.commit()
        return 200

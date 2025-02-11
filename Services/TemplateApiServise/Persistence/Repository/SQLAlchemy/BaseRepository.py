from typing import Sequence, Any, Literal

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import Row, RowMapping
from sqlalchemy.exc import IntegrityError

from Services.TemplateApiServise.Persistence.Database.DbContext import transaction


class BaseRepository[T, I]:

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
            return self.model(**data).add()
        except IntegrityError as error:
            logger.error(error)
            raise HTTPException(status_code=400, detail=f'{error}')

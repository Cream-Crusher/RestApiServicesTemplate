import logging
from datetime import datetime
from functools import wraps
from typing import Any, Sequence, Awaitable, Coroutine, Concatenate, Callable, Literal

from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import select, func, ScalarResult, Row, RowMapping
from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Shared.Base.Pagination import Pagination
from Shared.Sessions.session import AsyncDatabase


class BaseSqlAlchemyRepository[T, I]:

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def all(self, paging: Pagination = None) -> Sequence[Row | RowMapping | Any]:
        query = select(self.model).where(self.model.active.is_(True))  # type: ignore
        query = query.offset(paging.skip).limit(paging.limit) if paging else query
        result = await self.session.scalars(query)

        if not result:
            return []

        return result.all()

    async def id(self, model_id: I) -> T:
        model = await self.session.get(self.model, model_id)
        if model is not None:
            return model
        raise HTTPException(
            status_code=404,
            detail={"message": f'{self.model} by id "{model_id}" not found'}
        )

    async def create(self, data: dict | BaseModel) -> T:
        try:
            if isinstance(data, BaseModel):
                data = data.model_dump()

            model = self.model(**data)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except IntegrityError as error:
            logging.error(error)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "duplicate key value violates unique constraint"}
            )

    async def delete(self, model_id: I) -> Literal[200]:
        try:
            model = await self.id(model_id)
            if not model:
                raise HTTPException(
                    status_code=404,
                    detail={"message": f'{self.model} by id "{model_id}" not found'}
                )
            await self.session.delete(model)
            await self.session.commit()
            return 200
        except IntegrityError as error:
            logging.error(error)
            raise HTTPException(403, "There are links to other tables")
        except Exception as error:
            logging.error(error)
            raise HTTPException(500, f"{error}")

    async def update(self, model_id: I, update_data: dict | BaseModel) -> T:
        model = await self.id(model_id)

        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump()

        for key, value in update_data.items():
            if value is not None:
                attr_value = getattr(model, key)
                attr_value = attr_value.lower() if isinstance(attr_value, str) else attr_value
                validate_value = value.lower() if isinstance(value, str) else value
                if attr_value == validate_value:
                    continue
                else:
                    setattr(model, key, value)

        model.updated_at = datetime.utcnow()  # type: ignore
        self.session.add(model)
        await self.session.commit()

        return model

    async def filter(self, query: func) -> ScalarResult[T]:  # type: ignore
        result = (await self.session.execute(select(self.model).where(query))).scalar()

        if not result:
            raise HTTPException(404, 'objects not found')

        return result


#  todo для бота
def transaction[SELF, **P, T](
        func: Callable[Concatenate[SELF, AsyncSession, P], Awaitable[T]],
) -> Callable[Concatenate[SELF, P], Coroutine[Any, Any, T]]:
    @wraps(func)
    async def wrapped(self: SELF, *args: P.args, **kwargs: P.kwargs) -> T:
        if "session" in kwargs:
            session: AsyncSession = kwargs.pop("session")  # type: ignore
        else:
            session: AsyncSession = await AsyncDatabase.return_session()
        try:
            result = await func(self, session, *args, **kwargs)
        except DBAPIError:
            result = await func(self, session, *args, **kwargs)
        finally:
            if "session" not in kwargs:
                await session.close()
        return result

    return wrapped


class BaseSqlAlchemyTransactionRepository[T, I]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    @transaction
    async def all(self, session: AsyncSession) -> Sequence[T]:
        result = await session.scalars(select(self.model))
        return result.all()

    @transaction
    async def id(self, session: AsyncSession, model_id: I) -> T | None:
        model = await session.get(self.model, model_id)

        return model

    @transaction
    async def create(self, session: AsyncSession, data: T) -> T | None:
        try:
            model = self.model(**data.__dict__)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model
        except IntegrityError as e:
            logging.exception(e)
            return None

    @transaction
    async def delete(self, session: AsyncSession, model_id: I) -> Literal[200]:
        model = await self.id(model_id)
        await session.delete(model)
        await session.commit()
        return 200

    @transaction
    async def update(self, session: AsyncSession, model_id: I, update_data: dict) -> T | None:
        model = await self.id(model_id)
        for key, value in update_data.items():
            if value is not None:
                setattr(model, key, value)
        model.updated_at = datetime.utcnow()  # type: ignore
        session.add(model)
        await session.commit()
        return model

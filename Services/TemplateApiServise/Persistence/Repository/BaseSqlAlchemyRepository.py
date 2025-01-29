import logging
from typing import Sequence, Any, Union, List, Literal

from sqlalchemy import Row, RowMapping, select, func, ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Infrastructure.Pagination.Pagination import Pagination
from Services.TemplateApiServise.Persistence.Repository.BaseRepository import BaseRepository


class BaseSqlAlchemyRepository[T, I](BaseRepository):

    def __init__(self, session: AsyncSession, model: type[T]):
        super().__init__(model)
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

        if not model:
            raise Exception(f'{self.model} by id "{model_id}" not found')

        return model

    async def create(self, data: Union[T | List[T]]) -> Union[T | List[T] | None]:
        try:
            models, model = None, None
            if isinstance(data, List):
                models = data
                self.session.add_all(data)
            else:
                model = data
                self.session.add(data)

            await self.session.commit()

            return models if isinstance(data, list) else model

        except IntegrityError as e:
            logging.exception(e)
            raise Exception(f"model '{self.model}': {data}\n\nerror: {e}")

    async def delete(self, model_id: I) -> Literal[200]:
        try:
            model = await self.id(model_id)
            if not model:
                raise Exception(f'{self.model} by id "{model_id}" not found')

            await self.session.delete(model)
            await self.session.commit()
            return 200
        except IntegrityError as error:
            logging.error(error)
            raise Exception("There are links to other tables")
        except Exception as error:
            logging.error(error)
            raise Exception(f'{error}')

    async def update(self, model_id: I, update_data: I) -> T:
        model = await self.id(model_id)

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
            raise Exception('objects not found')

        return result

import logging
from typing import Sequence, Union, Iterable

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Infrastructure.Pagination.Pagination import Pagination


class BaseServise[T, I]:
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context

    def add(self, entity: T) -> T:
        self.db_context.add(entity)
        return entity

    async def add_range(self, entities: Iterable[T]) -> Iterable[T]:
        self.db_context.add_all(entities)

        return entities

    async def find(self, query: func) -> Sequence[T]:  # type: ignore
        result = (await self.db_context.execute(select(T).where(query))).scalars()
        assert result is not None, f"{T}: query '{query}' not found"

        return result.all()

    async def get_by_id(self, entity_id: I) -> T:
        entity = await self.db_context.get(T, entity_id)
        assert entity is not None, f"{T}: id '{entity_id}' not found"

        return entity

    async def get_all(self, paging: Pagination = None) -> Sequence[T]:
        query = select(T)
        query = (
            query
            .offset(paging.skip)
            .limit(paging.limit)
        ) if paging else query

        entities = await self.db_context.scalars(query)

        if not entities:
            return []

        return entities.all()

    async def remove(self, entity: Union[T | I]) -> None:
        try:
            if entity is I:
                entity = await self.get_by_id(entity)

            await self.db_context.delete(entity)

        except IntegrityError as error:
            logging.error(f'remove: {error}')
            raise Exception("There are links to other tables")

        except Exception as error:
            logging.error(f'remove: {error}')
            raise Exception(error)

    async def remove_range(self, entities: Iterable[Union[T | I]]) -> None:
        try:
            for entity in entities:
                if entity is I:
                    entity = await self.get_by_id(entity)

                await self.db_context.delete(entity)

        except IntegrityError as error:
            logging.error(f'remove_range: {error}')
            raise Exception("There are links to other tables")

        except Exception as error:
            logging.error(f'remove_range: {error}')
            raise Exception(error)

    async def update(self, new_entity: T, entity_id: Union[I | None] = None) -> T:
        entity = await self.get_by_id(entity_id if entity_id else new_entity.id)

        for key, value in new_entity.items():
            if value is not None:
                attr_value = getattr(entity, key)

                if attr_value == key:
                    continue
                else:
                    setattr(entity, key, value)

        entity.updated_at = datetime.utcnow()  # type: ignore
        self.db_context.add(entity)

        return entity

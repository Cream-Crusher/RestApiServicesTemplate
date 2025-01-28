from abc import ABC, abstractmethod
from typing import Any, Sequence, Literal, Union, overload, List

from pydantic import BaseModel
from sqlalchemy import func, ScalarResult, Row, RowMapping

from Infrastructure.Pagination.Pagination import Pagination


class BaseRepository[T, I](ABC):

    def __init__(self, model: type[T]) -> None:
        self.model = model

    @abstractmethod
    async def all(self, paging: Pagination = None) -> Sequence[Row | RowMapping | Any]:
        ...

    @abstractmethod
    async def id(self, model_id: I) -> T:
        ...

    @overload
    async def create(self, data: Union[dict | BaseModel]) -> T | None:
        ...

    @overload
    async def create(self, data: Union[list[dict] | list[BaseModel]]) -> List[T] | None:
        ...

    @abstractmethod
    async def create(self, data: Union[dict | BaseModel | list[dict] | list[BaseModel]]):
        ...

    @abstractmethod
    async def update(self, model_id: I, update_data: dict | BaseModel) -> T:
        ...

    @abstractmethod
    async def filter(self, query: func) -> ScalarResult[T]:
        ...

    @abstractmethod
    async def delete(self, model_id: I) -> Literal[200]:
        ...

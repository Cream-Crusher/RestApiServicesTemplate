from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseServise[T, I](ABC):

    def __init__(self, db_context: AsyncSession):
        self.db_context: AsyncSession = db_context

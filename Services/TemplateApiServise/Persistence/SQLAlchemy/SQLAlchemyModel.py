from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from Services.TemplateApiServise.Persistence.SQLAlchemy.SelectOfScalarExtended import SelectOfScalarExtended


class SQLAlchemyModel(DeclarativeBase):

    @classmethod
    def select(cls) -> "SelectOfScalarExtended[Self]":
        return SelectOfScalarExtended(cls)

    def add(self, db_context: AsyncSession):
        db_context.add(self)
        return self

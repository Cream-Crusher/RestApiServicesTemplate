from sqlalchemy.orm import DeclarativeBase

from Services.TemplateApiServise.Persistence.Database.DbContext import require_session
from Services.TemplateApiServise.Persistence.Repository.Orm.SQLAlchemyRepository import SQLAlchemyRepository


class SQLAlchemyModel(DeclarativeBase):

    @classmethod
    def select(cls) -> "SQLAlchemyRepository[Self]":
        return SQLAlchemyRepository(cls)

    def add(self) -> "SQLAlchemyModel":
        require_session().add(self)
        return self

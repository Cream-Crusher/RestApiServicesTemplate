from typing import Self

from sqlalchemy.orm import DeclarativeBase

from Services.TemplateApiServise.Persistence.Database.DbContext import get_session
from Services.TemplateApiServise.Persistence.Repository.Orm.SqlRepository import BaseRepository


class BaseSqlModel(DeclarativeBase):

    @classmethod
    def select(cls) -> "BaseRepository[Self]":
        return BaseRepository(cls)

    def add(self) -> "BaseSqlModel":
        get_session().add(instance=self)
        return self

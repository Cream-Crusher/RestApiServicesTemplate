import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel


class BaseEntity(BaseSqlModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

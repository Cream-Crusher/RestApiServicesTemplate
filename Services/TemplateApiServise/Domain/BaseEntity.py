import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel


class BaseEntity(BaseSqlModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

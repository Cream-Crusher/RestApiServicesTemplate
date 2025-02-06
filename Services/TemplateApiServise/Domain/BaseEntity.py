import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Persistence.SQLAlchemy.SQLAlchemyModel import SQLAlchemyModel
# todo небольшая погрешность чистой архитектуры т к это PyThOn


class BaseEntity(SQLAlchemyModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

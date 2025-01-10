import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    def to_dict(self) -> dict[str, Any]:
        return {c: getattr(self, c) for c in self.__table__.columns.keys()}

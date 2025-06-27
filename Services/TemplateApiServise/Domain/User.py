from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(type_=BIGINT, primary_key=True, nullable=False)  # type: ignore

    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name if self.last_name else ''}".strip()

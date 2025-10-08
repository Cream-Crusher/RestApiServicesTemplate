from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    is_manager: Mapped[bool] = mapped_column(server_default="false", nullable=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name if self.last_name else ''}".strip()

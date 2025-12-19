from enum import StrEnum

from sqlalchemy import VARCHAR, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


class UserRoleEnum(StrEnum):
    MODERATOR = "MODERATOR"
    USER = "USER"


class User(BaseEntity):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    role: Mapped[UserRoleEnum] = mapped_column(VARCHAR(16), server_default=UserRoleEnum.USER, nullable=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name if self.last_name else ''}".strip()

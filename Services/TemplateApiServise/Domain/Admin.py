from typing import Literal

from sqlalchemy.orm import Mapped, mapped_column

from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


class Admin(BaseEntity):
    __tablename__ = "admins"

    display_name: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=True)

    role: Mapped[Literal["admin", "super_admin"]] = mapped_column(default="admin", nullable=False)

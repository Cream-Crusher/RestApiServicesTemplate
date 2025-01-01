from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from Shared.Base.BaseModel import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(type_=BIGINT, primary_key=True, nullable=False)  # type: ignore

    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True)

from dataclasses import field
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    first_name:  str | None = None
    last_name: str | None = None
    username:  str | None = None


class UserRead(UserBase):
    pass


class UsersRead(BaseModel):
    users: List[UserRead] = field(default_factory=list)


class UserCreate(UserBase):
    pass

from typing import Literal

from pydantic import BaseModel, Field


class CreateAdminDTO(BaseModel):
    display_name: str = Field(min_length=5, max_length=64)
    password: str = Field(min_length=20, max_length=64)


class GetAdminByIdDTO(BaseModel):
    display_name: str
    role: Literal["admin", "super_admin"]

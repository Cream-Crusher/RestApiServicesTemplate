from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CreateAdminDTO(BaseModel):
    display_name: str = Field(min_length=5, max_length=64)
    password: str = Field(min_length=8, max_length=64)

    @field_validator("display_name", mode="before")
    def validate_display_name(cls, v):
        return v.strip()

    @field_validator("password", mode="before")
    def validate_password(cls, v):
        return v.strip()


class GetAdminByIdDTO(BaseModel):
    display_name: str
    role: Literal["admin", "super_admin"]

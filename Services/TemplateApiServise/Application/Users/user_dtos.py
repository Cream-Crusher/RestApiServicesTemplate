from pydantic import BaseModel, Field, field_validator


class GetUserByIdDTO(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None


class BaseUserDTO(BaseModel):
    first_name: str
    last_name: str | None = Field(default=None, min_length=1)
    username: str | None = Field(default=None, min_length=1)

    @field_validator("last_name", mode="before")
    def validate_last_name(cls, v):
        return v.strip()

    @field_validator("username", mode="before")
    def validate_username(cls, v):
        return v.strip()


class CreateUserDTO(BaseUserDTO): ...


class UpdateUserDTO(BaseUserDTO): ...

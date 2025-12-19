from pydantic import BaseModel


class GetUserByIdDTO(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None


class CreateUserDTO(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None


class UpdateUserDTO(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str | None = None

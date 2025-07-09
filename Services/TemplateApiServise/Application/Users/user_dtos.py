from pydantic import BaseModel


class GetUserByIdDTO(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str


class CreateUserDto(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str


class UpdateUserDto(BaseModel):
    first_name: str
    last_name: str | None = None
    username: str

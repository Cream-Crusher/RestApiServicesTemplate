from pydantic import BaseModel


class CreateUserDto(BaseModel):
    id: int
    first_name: str

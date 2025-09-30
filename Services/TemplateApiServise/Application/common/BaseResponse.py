from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: str = "success"
    detail: dict[str, str] | None = None

from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: str = "success"
    detail: dict[str, Any] | None = None

from fastapi import Request
from fastapi.responses import JSONResponse

from Services.TemplateApiServise.Application.exceptions.BaseApiError import BaseApiError


def base_api_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, BaseApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status,
                "error": exc.error,
                "message": exc.message,
                "detail": exc.detail,
            },
        )
    raise exc

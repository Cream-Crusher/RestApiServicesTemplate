import json

from fastapi import Request
from fastapi.responses import JSONResponse

from Services.TemplateApiServise.Application.common.exceptions.BaseApiError import BaseApiError
from Services.TemplateApiServise.Application.common.utils.JSONEncoder import JSONEncoder


def base_api_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, BaseApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": exc.success,
                "error": exc.error,
                "message": exc.message,
                "detail": json.loads(json.dumps(exc.detail, cls=JSONEncoder)),  # UUID TypeError handler
            },
        )
    raise exc

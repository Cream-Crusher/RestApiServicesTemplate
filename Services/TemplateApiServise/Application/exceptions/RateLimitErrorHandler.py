from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from Services.TemplateApiServise.Application.exceptions.RateLimitError import RateLimitError


def rate_limit_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RateLimitError):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "status": "error",
                "error": "TOO_MANY_REQUESTS",
                "message": f"Too Many Requests by {exc.key}",
                "detail": {"key": exc.key, "rps_limit": exc.max_calls / exc.period_seconds},
            },
        )
    raise exc

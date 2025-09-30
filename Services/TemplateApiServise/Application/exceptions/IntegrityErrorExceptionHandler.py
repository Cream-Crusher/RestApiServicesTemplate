from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette import status


def integrity_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "error": "IntegrityError", "message": exc.orig, "detail": None},
        )
    raise exc

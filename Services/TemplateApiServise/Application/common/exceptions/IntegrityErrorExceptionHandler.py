from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette import status


def integrity_error_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, IntegrityError):
        error = "INTEGRITY_ERROR"
        orig = exc.orig.__str__()
        if "duplicate key" in orig:
            error = "DUPLICATE_KEY"
        elif "foreign key" in orig:
            error = "FOREIGN_KEY"

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "error": error, "message": "integrity error", "detail": {"orig": orig}},
        )
    raise exc

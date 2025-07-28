from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette import status


def integrity_error_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, IntegrityError):
        error_message = str(exc.orig)
        table_name = error_message.split('"')[1].replace("_unique", "") if '"' in error_message else "Model"
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "message": f"{table_name} recorded already exists"},
        )
    raise exc

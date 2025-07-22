from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound


def model_not_found_error_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ModelNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )
    raise exc

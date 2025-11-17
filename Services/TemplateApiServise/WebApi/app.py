from typing import Literal

import uvicorn
from fastapi import APIRouter, FastAPI
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware
from starlette_context import middleware, plugins

from config import EnvironmentEnum, settings
from Services.TemplateApiServise.Application.exceptions.BaseApiError import BaseApiError
from Services.TemplateApiServise.Application.exceptions.BaseApiErrorHandler import base_api_error_handler
from Services.TemplateApiServise.Application.exceptions.IntegrityErrorExceptionHandler import integrity_error_handler
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import (
    ModelNotFound,
)
from Services.TemplateApiServise.Application.exceptions.ModelNotFoundHandler import model_not_found_error_handler
from Services.TemplateApiServise.WebApi.Controllers.AdminController import admins_router
from Services.TemplateApiServise.WebApi.Controllers.S3Controller import simple_storage_service_router
from Services.TemplateApiServise.WebApi.Controllers.UserController import users_router

# add FastApi
if settings.app_config.environment == EnvironmentEnum.PROD:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(docs_url="/swagger")

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)
app.add_middleware(
    middleware_class=middleware.ContextMiddleware,
    plugins=(plugins.ForwardedForPlugin(),),
)

router = APIRouter(prefix="/api/v1")


@router.get("/ping", tags=["Server"])
async def ping_server() -> Literal["pong"]:
    return "pong"


# Server
app.include_router(router, tags=["Server"], prefix="/server")
# User
app.include_router(users_router, tags=["User | Users"], prefix=f"{router.prefix}/users")
# Admin
app.include_router(admins_router, tags=["Admin | Admins"], prefix=f"{router.prefix}/admins")
# s3
app.include_router(simple_storage_service_router, tags=["S3 | Simple Storage Service"], prefix=f"{router.prefix}/s3")

# Exceptions Handlers
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(ModelNotFound, model_not_found_error_handler)
app.add_exception_handler(BaseApiError, base_api_error_handler)


# uvicorn
config = uvicorn.Config(
    app,
    host="0.0.0.0",
    port=8011,
    reload=True,
)
uvicorn_server = uvicorn.Server(config=config)

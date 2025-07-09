from typing import Literal

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware

from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound
from Services.TemplateApiServise.Application.exceptions.ModelNotFoundHandler import \
    model_not_found_error_exception_handler
from Services.TemplateApiServise.Application.exceptions.integrity_error_exception_handler import \
    integrity_error_exception_handler
from Services.TemplateApiServise.WebApi.Controllers.UserController import users_router
from config import settings

# add FastApi
if settings.app_config.environment_type == 'prod':
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(docs_url="/swagger", redoc_url=None)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

router = APIRouter(prefix='/api/v1')


@router.get("/ping", tags=["Server"])
async def ping_server() -> Literal["pong"]:
    return "pong"


# Server
app.include_router(router, tags=['Server'], prefix='/server')
# User
app.include_router(users_router, tags=['User | Users'], prefix=f'{router.prefix}/users')


# Exceptions Handlers
app.add_exception_handler(IntegrityError, integrity_error_exception_handler)
app.add_exception_handler(ModelNotFound, model_not_found_error_exception_handler)


# uvicorn
config = uvicorn.Config(
    app,
    host="0.0.0.0",
    port=8011,
    reload=True,
)
uvicorn_server = uvicorn.Server(config=config)

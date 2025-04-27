import logging

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Services.TemplateApiServise.WebApi.Controllers.UserController import users_router
from config import settings


# add logging
logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# add FastApi
if settings.api_servise_config.dev:
    app = FastAPI(docs_url="/swagger", redoc_url=None)
else:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

router = APIRouter(prefix='/api/v1')


@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


# Server
app.include_router(router, tags=['Server'], prefix='server')
# User
app.include_router(users_router, tags=['User | Users'], prefix=f'{router.prefix}/users')
# router.include_router(users_router, tags=['User | Users'], prefix='/users')


# TODO отключение документации для прода
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=422,
#         content={"detail": "Произошла ошибка. Пожалуйста, проверьте данные."}
#     )
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content={"detail": "Некорректные данные. Пожалуйста, проверьте введенные данные."}
#     )


# uvicorn
config = uvicorn.Config(
    app,
    host="0.0.0.0",
    port=8011,
    reload=True,
)
uvicorn_server = uvicorn.Server(config=config)

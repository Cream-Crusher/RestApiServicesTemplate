import logging

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Services.TemplateApiServise.WebApi.Controllers.UserController import users_router
from Services.TemplateApiServise.WebApi.config import settings

# add AsyncIOScheduler
scheduler = AsyncIOScheduler()

# add logging
logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# add FastApi
app = FastAPI(docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

# add FastApi
if settings.api_servise_config.dev:
    app = FastAPI(docs_url="/swagger", redoc_url=None)
else:
    app = FastAPI(openapi_url=None)


router = APIRouter()
# User
app.include_router(users_router, tags=['User | Users'], prefix='/users')
# router.include_router(users_router, tags=['User | Users'], prefix='/users')


@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


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


app.include_router(router, prefix='/api/v1')

# uvicorn
config = uvicorn.config.Config(
    app,
    host="0.0.0.0",
    port=8011,
    reload=True,
)
uvicorn_server = uvicorn.Server(config=config)

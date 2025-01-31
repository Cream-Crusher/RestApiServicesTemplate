import logging

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Services.TemplateApiServise.WebApi.Controllers.UserController import users_router

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

router = APIRouter()
# User
app.include_router(users_router, tags=['User | Users'], prefix='/users')
# router.include_router(users_router, tags=['User | Users'], prefix='/users')


@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


app.include_router(router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8011, reload=True)


# TODO отключение документации, если нужно
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

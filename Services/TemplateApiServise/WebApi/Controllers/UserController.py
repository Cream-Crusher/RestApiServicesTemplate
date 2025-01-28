from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from Services.TemplateApiServise.Application.Users.IUserService import IUserService
from Services.TemplateApiServise.Application.Users.user_dto import CreateUserDto

users_router = APIRouter(route_class=DishkaRoute)


@users_router.post('/', name='create', status_code=201)
async def create(
        user_create_dto: CreateUserDto,
        user_service: FromDishka[IUserService]
):
    await user_service.create(user_create_dto)

    return JSONResponse(
        content={"message": "Success"},
        status_code=status.HTTP_201_CREATED,
        media_type="application/json"
    )

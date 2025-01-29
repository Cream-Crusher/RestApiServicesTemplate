from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from Services.TemplateApiServise.Application.Users.UserService import UserService, user_service
from Services.TemplateApiServise.Application.Users.user_dto import CreateUserDto

users_router = APIRouter()


@users_router.post('/', name='create', status_code=201)
async def create(
        user_create_dto: CreateUserDto,
        user_service: UserService = user_service
):
    await user_service.create(user_create_dto)

    return JSONResponse(
        content={"message": "Success"},
        status_code=status.HTTP_201_CREATED,
        media_type="application/json"
    )

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from Services.TemplateApiServise.Application.Users.UserService import user_service
from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto

users_router = APIRouter()


@users_router.post(path='/', name='create', status_code=status.HTTP_201_CREATED)
async def create(
        user_create_dto: CreateUserDto,
) -> JSONResponse:
    await user_service.create(data=user_create_dto.__dict__)

    return JSONResponse(
        content={"message": "Success"},
        status_code=status.HTTP_201_CREATED,
        media_type="application/json"
    )

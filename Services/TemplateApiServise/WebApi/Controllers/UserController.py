from fastapi import APIRouter
from fastapi import status

from Services.TemplateApiServise.Application.Users.UserService import user_service
from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto
from Services.TemplateApiServise.Application.common.BaseResponse import BaseResponse
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction

users_router = APIRouter()


@users_router.post(
    path='',
    name='create',
    status_code=status.HTTP_201_CREATED
)
@transaction()  # type: ignore
async def create_user_api(
        user_create_dto: CreateUserDto,
) -> BaseResponse:
    await user_service.create(data=user_create_dto.model_dump())

    return BaseResponse(success=True)

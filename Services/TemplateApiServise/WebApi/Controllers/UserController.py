from fastapi import APIRouter, status

from Services.TemplateApiServise.Application.common.BaseResponse import BaseResponse
from Services.TemplateApiServise.Application.Users.user_dtos import (
    CreateUserDTO,
    GetUserByIdDTO,
    UpdateUserDTO,
)
from Services.TemplateApiServise.Application.Users.UserCommandService import (
    user_command_service,
)
from Services.TemplateApiServise.Application.Users.UserQueryService import (
    user_query_service,
)
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction

users_router = APIRouter()


@users_router.get(
    path="/{user_id}",
    name="get user by id",
    status_code=status.HTTP_200_OK,
    response_model=GetUserByIdDTO,
)
@transaction()  # type: ignore
async def get_user_by_id_api(
    user_id: int,
) -> GetUserByIdDTO:
    return await user_query_service.get_by_id(user_id)


@users_router.post(path="", name="create user", status_code=status.HTTP_201_CREATED)
@transaction()  # type: ignore
async def create_user_api(
    new_user_dto: CreateUserDTO,
) -> BaseResponse:
    user_command_service.create(new_user_dto)

    return BaseResponse(success=True)


@users_router.put(path="/{user_id}", name="update user", status_code=status.HTTP_200_OK)
@transaction()  # type: ignore
async def update_user_api(
    user_id: int,
    update_user_dto: UpdateUserDTO,
) -> BaseResponse:
    await user_command_service.update(user_id, update_user_dto, f"user:{user_id}")

    return BaseResponse(success=True)


@users_router.delete(path="/{user_id}", name="delete user", status_code=status.HTTP_200_OK)
@transaction()  # type: ignore
async def delete_user_api(
    user_id: int,
) -> BaseResponse:
    await user_command_service.delete(user_id, f"user:{user_id}")

    return BaseResponse(success=True)

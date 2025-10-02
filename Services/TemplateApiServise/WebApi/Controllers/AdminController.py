from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from Services.TemplateApiServise.Application.Admins.admin_dtos import CreateAdminDTO
from Services.TemplateApiServise.Application.Admins.AdminCommandService import admin_command_service
from Services.TemplateApiServise.Application.auth.Oauth2Authorization import AdminDTO, get_me_admin
from Services.TemplateApiServise.Application.common.BaseResponse import BaseResponse
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction

admins_router = APIRouter()


@admins_router.post(path="/register", name="create admin", status_code=status.HTTP_201_CREATED)
@transaction()
async def create_admin_api(create_admin_dto: CreateAdminDTO, admin: AdminDTO = Depends(get_me_admin)) -> BaseResponse:
    await admin_command_service.create_admin(admin, create_admin_dto)
    return BaseResponse()


@admins_router.post("/login", name="login", status_code=200)
@transaction()
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    return await admin_command_service.login(form_data)

import uuid

from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from Services.TemplateApiServise.Application.Admins.admin_dtos import CreateAdminDTO
from Services.TemplateApiServise.Application.auth.Oauth2Authorization import (
    AdminDTO,
    create_access_token,
    hash_password,
    verify_password,
)
from Services.TemplateApiServise.Application.common.BaseCommandService import BaseCommandService
from Services.TemplateApiServise.Application.exceptions.BaseApiError import BaseApiError
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound
from Services.TemplateApiServise.Domain.Admin import Admin


class AdminCommandService(BaseCommandService[Admin, uuid.UUID]):

    def __init__(self):
        super().__init__(model=Admin)

    async def create_admin(self, admin: AdminDTO, create_admin_user_dto: CreateAdminDTO):
        real_admin = await Admin.select().where(Admin.id == admin.id).one_or_raise(ModelNotFound(Admin))
        if real_admin.role != "super_admin":
            raise BaseApiError(403, error="Forbidden", message=f"Admin {admin.id} is not super_admin role")

        self.model(
            display_name=create_admin_user_dto.display_name,
            password_hash=hash_password(create_admin_user_dto.password),
            role="admin",
        ).add()

        await self.cache_service.delete(keys="admins:all")

    async def login(self, login: OAuth2PasswordRequestForm) -> JSONResponse:
        username, password = login.username, login.password
        real_admin: Admin = (
            await self.model.select().where(Admin.display_name == username).one_or_raise(ModelNotFound(Admin))
        )

        if not verify_password(password, real_admin.password_hash):
            raise BaseApiError(403, error="Forbidden", message="Invalid password")

        access_token = create_access_token(AdminDTO(id=real_admin.id, display_name=real_admin.display_name))

        response = JSONResponse(content={"access_token": access_token, "type": "bearer"})
        response.set_cookie(key="access_token", value=access_token, secure=True, samesite="none")
        response.headers["Authorization"] = f"Bearer {access_token}"

        return response


admin_command_service = AdminCommandService()

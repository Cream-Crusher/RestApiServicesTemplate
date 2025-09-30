import uuid
from collections.abc import Iterable

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from Services.TemplateApiServise.Application.Admins.admin_dtos import CreateAdminDTO, GetAssessTokenDTO
from Services.TemplateApiServise.Application.auth.Oauth2Authorization import (
    AdminDTO,
    create_access_token,
    hash_password,
    verify_password,
)
from Services.TemplateApiServise.Application.common.BaseCommandService import BaseCommandService
from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService, model_cache_service
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound
from Services.TemplateApiServise.Domain.Admin import Admin


class AdminCommandService(BaseCommandService[Admin, uuid.UUID]):

    def __init__(self, cache_service: ModelCacheService = model_cache_service):
        super().__init__(model=Admin, cache_service=cache_service)

    async def create_admin(self, create_admin_user_dto: CreateAdminDTO, keys: Iterable[str] | str | None = None):
        self.model(
            display_name=create_admin_user_dto.display_name,
            password_hash=hash_password(create_admin_user_dto.password),
            role="admin",
        ).add()

        if keys:
            await self.cache_service.delete(keys=keys)

    async def login(self, login: OAuth2PasswordRequestForm) -> GetAssessTokenDTO:
        username, password = login.username, login.password
        real_admin: Admin = (
            await self.model.select().where(Admin.display_name == username).one_or_raise(ModelNotFound(Admin))
        )

        if not verify_password(password, real_admin.password_hash):
            raise HTTPException(403, "Invalid password")

        assess_token = create_access_token(AdminDTO(id=real_admin.id, display_name=real_admin.display_name))

        return GetAssessTokenDTO(access_token=assess_token, type="bearer")


admin_command_service = AdminCommandService()

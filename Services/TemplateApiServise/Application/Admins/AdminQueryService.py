from Services.TemplateApiServise.Application.Admins.admin_dtos import GetAdminByIdDTO
from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService, model_cache_service
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound
from Services.TemplateApiServise.Domain.Admin import Admin


class AdminQueryService:

    def __init__(self, cache_service: ModelCacheService = model_cache_service):
        self.cache_service = cache_service

    async def get_by_id(self, admin_id: int) -> GetAdminByIdDTO:
        cached_key = f"admin:{admin_id}"
        cached_model = await self.cache_service.get(key=cached_key, callback=GetAdminByIdDTO)

        if cached_model:
            return cached_model

        real_admin = await Admin.select().where(Admin.id == admin_id).one_or_raise(ModelNotFound(Admin))
        return_real_admin = GetAdminByIdDTO(**real_admin.__dict__)
        await self.cache_service.set(cached_key, return_real_admin)

        return return_real_admin


admin_query_service = AdminQueryService()

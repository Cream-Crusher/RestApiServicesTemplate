import uuid

from Services.TemplateApiServise.Application.common.BaseQueryService import BaseQueryService
from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService, model_cache_service
from Services.TemplateApiServise.Domain.Admin import Admin


class AdminQueryService(BaseQueryService[Admin, uuid.UUID]):

    def __init__(self, cache_service: ModelCacheService = model_cache_service):
        super().__init__(model=Admin, cache_service=cache_service)


admin_query_service = AdminQueryService()

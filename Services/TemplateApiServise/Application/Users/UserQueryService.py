from Services.TemplateApiServise.Application.common.BaseQueryService import BaseQueryService
from Services.TemplateApiServise.Application.common.ModelCacheService import (
    ModelCacheService,
    model_cache_service,
)
from Services.TemplateApiServise.Domain.User import User


class UserQueryService(BaseQueryService[User, int]):

    def __init__(self, cache_service: ModelCacheService = model_cache_service):
        super().__init__(model=User, cache_service=cache_service)


user_query_service = UserQueryService()

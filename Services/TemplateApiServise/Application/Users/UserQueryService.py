from Infrastructure.Profiler.profiler import profiler
from Services.TemplateApiServise.Application.common.ModelCacheService import (
    ModelCacheService,
    model_cache_service,
)
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import (
    ModelNotFound,
)
from Services.TemplateApiServise.Application.Users.user_dtos import GetUserByIdDTO
from Services.TemplateApiServise.Domain.User import User


class UserQueryService:

    def __init__(self, cache_service: ModelCacheService = model_cache_service):
        self.cache_service = cache_service

    @profiler("UserQueryService_")
    async def get_by_id(self, user_id: int) -> GetUserByIdDTO:
        cached_key = f"user:{user_id}"
        cached_model = await self.cache_service.get(key=cached_key, callback=GetUserByIdDTO)

        if cached_model:
            return cached_model

        real_user: User = await User.select().where(User.id == user_id).one_or_raise(ModelNotFound(User))
        return_real_user = GetUserByIdDTO(**real_user.__dict__)
        await self.cache_service.set(cached_key, return_real_user)

        return return_real_user


user_query_service = UserQueryService()

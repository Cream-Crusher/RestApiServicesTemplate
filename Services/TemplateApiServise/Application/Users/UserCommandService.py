from Services.TemplateApiServise.Application.common.BaseCommandService import (
    BaseCommandService,
)
from Services.TemplateApiServise.Application.common.ModelCacheService import (
    ModelCacheService,
    model_cache_service,
)
from Services.TemplateApiServise.Domain.User import User


class UserCommandService(BaseCommandService[User, int]):

    def __init__(self, cache_service: ModelCacheService = model_cache_service):
        super().__init__(model=User, cache_service=cache_service)


user_command_service = UserCommandService()

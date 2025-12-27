from Services.TemplateApiServise.Application.common.BaseQueryService import BaseQueryService
from Services.TemplateApiServise.Domain.User import User


class UserQueryService(BaseQueryService[User, int]):

    def __init__(self):
        super().__init__(model=User)


user_query_service = UserQueryService()

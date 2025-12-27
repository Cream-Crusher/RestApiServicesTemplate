from Services.TemplateApiServise.Application.common.BaseCommandService import (
    BaseCommandService,
)
from Services.TemplateApiServise.Domain.User import User


class UserCommandService(BaseCommandService[User, int]):

    def __init__(self):
        super().__init__(model=User)


user_command_service = UserCommandService()

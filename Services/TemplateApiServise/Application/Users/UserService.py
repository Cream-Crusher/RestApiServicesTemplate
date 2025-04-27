import uuid
from typing import Union

from Services.TemplateApiServise.Application.common.BaseService import BaseService
from Services.TemplateApiServise.Domain.User import User


class UserService(BaseService[User, Union[int, uuid.UUID]]):

    def __init__(self):
        super().__init__(model=User)


user_service: UserService = UserService()

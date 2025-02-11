from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Repository.SQLAlchemy.BaseRepository import BaseRepository


class UserService(BaseRepository[User, int]):

    def __init__(self):
        super().__init__(model=User)


user_service: UserService = UserService()

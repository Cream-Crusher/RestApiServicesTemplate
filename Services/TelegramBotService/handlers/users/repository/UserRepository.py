from Services.User.Users.model import User
from Services.TemplateApiServise.Persistence.Repository.BaseRepository import BaseSqlAlchemyTransactionRepository


class UserRepository(BaseSqlAlchemyTransactionRepository[User, int]):

    def __init__(self, model: type[User]) -> None:
        super().__init__(model)


UserRep = UserRepository(model=User)

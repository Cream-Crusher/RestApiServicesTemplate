from Services.TemplateApiServise.Persistence.Repository.BaseS3Repository import BaseSqlAlchemyTransactionRepository
from Services.User.Users.model import User


class UserRepository(BaseSqlAlchemyTransactionRepository[User, int]):

    def __init__(self, model: type[User]) -> None:
        super().__init__(model)


UserRep = UserRepository(model=User)

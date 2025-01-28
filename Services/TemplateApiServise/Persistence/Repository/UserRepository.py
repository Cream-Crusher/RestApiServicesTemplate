from sqlalchemy.ext.asyncio import AsyncSession

from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Repository.BaseSqlAlchemyRepository import BaseSqlAlchemyRepository


class UserRepository(BaseSqlAlchemyRepository[User, int]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model=User)

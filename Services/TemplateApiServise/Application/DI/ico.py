from dishka import Provider, from_context, Scope, provide, make_async_container
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.TemplateApiServise.Application.Users.IUserService import IUserService
from Services.TemplateApiServise.Application.Users.UserService import UserService
from Services.TemplateApiServise.Persistence.Database.sqlalchemy_session import AsyncDatabase
from Services.TemplateApiServise.Persistence.Repository.UserRepository import UserRepository


class RepoProvider(Provider):

    user_repository = from_context(provides=UserRepository, scope=Scope.APP)

    @provide(scope=Scope.APP)  # todo вынести в di Persistence
    async def get_user_repository(self, session: AsyncSession = Depends(AsyncDatabase.get_session)) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.APP)
    async def get_user_service(self, user_repository: UserRepository = Depends(get_user_repository)) -> IUserService:
        return UserService(user_repository)


container = make_async_container(
    RepoProvider()
)
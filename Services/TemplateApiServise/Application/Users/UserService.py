from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto
from Services.TemplateApiServise.Application.common.mapping import mapping
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction


class UserService:

    @transaction()
    async def create(self, user_dto: CreateUserDto) -> User:
        user_model: User = mapping(from_data=user_dto, to=User)
        user_model.add()
        query = await User.select().where(User.id == user_model.id).all()

        return user_model


user_service: UserService = UserService()

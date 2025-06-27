from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo
from async_lru import alru_cache

from Infrastructure.Posthog.Posthog import posthog_manager
from Services.TelegramBotService.BotMiddlewares.UserMW import TelegramUser
from Services.TelegramBotService.handlers.users.texts.start_text import StartText
from Services.TelegramBotService.utils.keyboard.ikb import IKB
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction

router = Router()


@alru_cache()
async def get_user(user_id: str) -> User:
    return await User.select().where(User.id == user_id).one_or_raise(AssertionError(f'User {user_id} not found'))


@router.message(Command("start"))
@transaction()  # type: ignore
async def start(message: Message, command: CommandObject, state: FSMContext, telegram_user: TelegramUser):
    await state.clear()
    user_id: int | str = telegram_user.id
    try:
        await get_user()
    except AssertionError:
        User(**telegram_user.model_dump()).add()
        await posthog_manager.lead_register(user_id=str(user_id), referral=command.args, user_data=message.chat.model_dump())  # type: ignore

    await posthog_manager.lead_state(user_id=str(user_id), state='start')

    await message.answer(
        text=StartText.start,
        reply_markup=IKB()
        .row(text="Перейти в игру1", web_app=WebAppInfo(url='https://www.littlerockzoo.com/media/2908/2022-0104-red-fox-james-syler.jpg'))
    )

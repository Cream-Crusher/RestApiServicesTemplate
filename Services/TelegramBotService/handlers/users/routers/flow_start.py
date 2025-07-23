from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo

from config import settings
from Infrastructure.Posthog.Posthog import posthog_manager
from Services.TelegramBotService.BotMiddlewares.UserMW import TelegramUser
from Services.TelegramBotService.handlers.users.texts.start_text import StartText
from Services.TelegramBotService.utils.keyboard.ikb import IKB
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import (
    ModelNotFound,
)
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction
from Services.TemplateApiServise.WebApi.Controllers.UserController import get_user_by_id_api  # type: ignore

router = Router()


@router.message(Command("start"))
@transaction()  # type: ignore
async def start(
    message: Message,
    command: CommandObject,
    state: FSMContext,
    telegram_user: TelegramUser,
):
    await state.clear()
    user_id: int | str = telegram_user.id
    try:
        await get_user_by_id_api(user_id)  # type: ignore
    except ModelNotFound:
        User(**telegram_user.model_dump()).add()
        await posthog_manager.lead_register(user_id=str(user_id), referral=command.args, user_data=message.chat.model_dump())  # type: ignore

    await posthog_manager.lead_state(user_id=str(user_id), state="start")

    await message.answer(
        text=StartText.start,
        reply_markup=IKB().row(
            text="Перейти в игру1",
            web_app=WebAppInfo(url=settings.bot_config.web_app_url),  # type: ignore
        ),  # type: ignore
    )

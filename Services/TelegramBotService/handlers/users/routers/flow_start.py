from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo

from Infrastructure.Posthog.Posthog import PosthogMan
from Services.TelegramBotService.handlers.users.texts.start_text import StartText
from Services.TelegramBotService.utils.keyboard.ikb import IKB
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import require_session, transaction

router = Router()


@router.message(Command("start"))
@transaction()
async def start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    user = message.chat.model_dump()  # type: ignore

    user_model = await User.select().where(User.id == user['id']).one_or_none()
    if user_model is None:
        session = require_session()
        User(**user).add()
        await session.commit()
        await PosthogMan.lead_start(str(user['id']), command.args, message.chat)  # type: ignore

    await PosthogMan.lead_state(str(user['id']), 'start')

    await message.answer(
        text=StartText.start,
        reply_markup=IKB()
        .row("Перейти в игру1", web_app=WebAppInfo(url='https://www.littlerockzoo.com/media/2908/2022-0104-red-fox-james-syler.jpg'))
    )

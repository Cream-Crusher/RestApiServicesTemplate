from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo
from sqlalchemy.ext.asyncio.session import AsyncSession

from Infrastructure.Posthog.Posthog import posthog_manager
from Services.TelegramBotService.BotMiddlewares.UserMW import TelegramUser
from Services.TelegramBotService.handlers.users.texts.start_text import StartText
from Services.TelegramBotService.utils.keyboard.ikb import IKB
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import require_session, transaction

router = Router()


@router.message(Command("start"))
@transaction()  # type: ignore
async def start(message: Message, command: CommandObject, state: FSMContext, telegram_user: TelegramUser):
    await state.clear()
    user_id: int | str = telegram_user.id
    user_model: User | None = await User.select().where(User.id == user_id).one_or_none()

    if user_model is None:
        session: AsyncSession = require_session()
        User(**telegram_user.model_dump()).add()
        await session.commit()
        await posthog_manager.lead_start(user_id=str(user_id), referral=command.args, user=message.chat)  # type: ignore

    await posthog_manager.lead_state(user_id=str(user_id), state='start')

    await message.answer(
        text=StartText.start,
        reply_markup=IKB()
        .row(text="Перейти в игру1", web_app=WebAppInfo(url='https://www.littlerockzoo.com/media/2908/2022-0104-red-fox-james-syler.jpg'))
    )

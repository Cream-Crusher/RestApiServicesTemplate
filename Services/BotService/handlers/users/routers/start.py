from aiogram import Router
from aiogram.filters import CommandObject, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo

from Services.BotService.handlers.users.repository.UserRepository import UserRep
from Services.BotService.handlers.users.texts.start import StartText
from Services.BotService.utils.keyboard.ikb import IKB
from Services.UserService.Users.schema import UserCreate
from Shared.Integrations.Posthog import PosthogMan

router = Router()


@router.message(Command("start"))
async def start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    user = message.chat.model_dump()  # type: ignore

    if await UserRep.id(user['id']) is None:
        await UserRep.create(UserCreate(**user))  # type: ignore

    await PosthogMan.lead_start(str(user['id']), command.args, message.chat)  # type: ignore
    await PosthogMan.lead_state(str(user['id']), 'start')

    await message.answer(
        text=StartText.start,
        reply_markup=IKB()
        .row("Перейти в игру1", web_app=WebAppInfo(url='https://www.littlerockzoo.com/media/2908/2022-0104-red-fox-james-syler.jpg'))
    )

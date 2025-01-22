import asyncio
from contextlib import suppress

from aiogram import Router, types
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo

from Services.BotService.handlers.manager.filters.tools import ManagerFilter
from Services.BotService.handlers.manager.keyboards.commands.tool import ToolKeyboardsCommands
from Services.BotService.handlers.manager.states.tool import ToolState
from Services.BotService.handlers.manager.texts.tool import ToolText
from Services.BotService.handlers.users.repository.UserRepository import UserRep
from Services.BotService.utils.keyboard.kb import IKB
from Shared.Integrations.Posthog import PosthogMan
from Shared.Middlewares.BotMiddlewares.UserMW import TelegramUser

router = Router()


@router.message(Command("/"), ManagerFilter())  # todo get file id
async def tool(message: Message, state: FSMContext):
    if message.from_user.id == 1001631806:
        await state.set_state(ToolState.tool)


@router.message(ToolState.tool)
async def tool(message: Message):
    if message.voice:
        await message.answer(message.voice.file_id)
    elif message.document:
        await message.answer(message.document.file_id)
    elif message.photo:
        await message.answer(message.photo[0].file_id)
    elif message.video_note:
        await message.answer(message.video_note.file_id)
    elif message.video:
        await message.answer(message.video.file_id)
    elif message.sticker:
        await message.answer(message.sticker.file_id)


@router.message(Command("send_broadcast"), ManagerFilter())  # todo malling
async def tool(message: Message, state: FSMContext):
    await state.set_state(ToolState.start_mallin)
    await message.answer("Отправьте сообщение, которое надо разослать")


@router.message(ToolState.start_mallin)  # TODO служебное
async def tool(message: Message, state: FSMContext, telegram_user: TelegramUser):
    await state.update_data(message_id=message.message_id)
    await state.set_state(ToolState.send_broadcast)

    data = await state.get_data()
    message_id = data.get('message_id')
    await message.bot.copy_message(
        from_chat_id=telegram_user.id,
        chat_id=telegram_user.id,
        message_id=message_id,
        parse_mode='HTML',
    )
    await message.answer(
        ToolText.mailing_confirmation,
        reply_markup=ToolKeyboardsCommands.mailing_confirmation_kb
    )


@router.message(ToolState.send_broadcast)  # TODO служебное
async def tool(message: Message, state: FSMContext, telegram_user: TelegramUser):
    if message.text == "yes":
        await PosthogMan.lead_state(str(telegram_user.id), "mailing_admin", telegram_user.model_dump())
        await message.answer(ToolText.mailing_confirmated)
        data = await state.get_data()
        message_id = data.get('message_id')
        users = await UserRep.all()

        async def send_message(message: types.Message, chat_id: str):
            with suppress(Exception):
                message_data = await message.bot.copy_message(
                    from_chat_id=telegram_user.id,
                    chat_id=chat_id,
                    message_id=message_id,
                    parse_mode='HTML',
                )

                await PosthogMan.lead_state(chat_id, "send_broadcast", message_data.model_dump())

        tasks = []
        for user in users:
            tasks.append(asyncio.create_task(send_message(message, str(user.id))))

        await asyncio.gather(*tasks)
        await message.answer(ToolText.mailing_end)
    else:
        await message.answer(ToolText.mailing_canceled)

    await state.clear()


@router.message(Command("wa"))
async def webapp(message: Message, command: CommandObject):
    assert command.args
    await message.answer(
        'TestWaLink',
        reply_markup=IKB()
        .row('TestWaLinkKB', web_app=WebAppInfo(url=command.args))
    )

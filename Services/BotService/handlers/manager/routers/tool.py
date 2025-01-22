import asyncio
from contextlib import suppress

from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext

from Services.BotService.handlers.manager.filters.tools import ManagerFilter
from Services.BotService.handlers.manager.keyboards.callbacks.tool import ToolKeyboardsCallbacks
from Services.BotService.handlers.manager.keyboards.commands.tool import ToolKeyboardsCommands
from Services.BotService.handlers.manager.states.tool import ToolState
from Services.BotService.handlers.manager.texts.tool import ToolText
from Services.BotService.handlers.users.repository.UserRepository import UserRep
from Shared.Integrations.Posthog import PosthogMan
from Shared.Middlewares.BotMiddlewares.UserMW import TelegramUser

router = Router()


@router.message(filters.Command("start_tool"), filters.StateFilter("*"), ManagerFilter())  # todo get file id
async def tool(message: types.Message, state: FSMContext):
    if message.from_user.id == 1001631806:
        await state.set_state(ToolState.tool)


@router.message(filters.StateFilter(ToolState.tool))
async def tool(message: types.Message):
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


@router.message(filters.Command("send_broadcast"), filters.StateFilter("*"), ManagerFilter())  # todo malling
async def tool(message: types.Message, state: FSMContext):
    await state.set_state(ToolState.start_mallin)
    await message.answer("Отправьте сообщение, которое надо разослать")


@router.message(filters.StateFilter(ToolState.start_mallin))  # TODO служебное
async def tool(message: types.Message, state: FSMContext, telegram_user: TelegramUser):
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
    await message.answer(ToolText.mailing_confirmation, reply_markup=ToolKeyboardsCommands.mailing_confirmation_kb)


@router.message(filters.StateFilter(ToolState.send_broadcast))  # TODO служебное
async def tool(message: types.Message, state: FSMContext, telegram_user: TelegramUser):
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


@router.message(filters.Command("wa"), filters.StateFilter("*"))
async def start(message: types.Message):
    link = message.text.replace('/wa', '').strip()
    await message.answer('start_test_url', reply_markup=ToolKeyboardsCallbacks.web_kb('wa_link', link))

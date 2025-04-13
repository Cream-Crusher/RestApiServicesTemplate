from contextlib import suppress
from typing import Any, Sequence
import anyio
from aiogram import Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo, MessageId

from Services.TelegramBotService.handlers.manager.filters.tools_filters import ManagerFilter
from Services.TelegramBotService.handlers.manager.states.tool_state import ToolState
from Services.TelegramBotService.handlers.manager.texts.tool_text import ToolText
from Services.TelegramBotService.utils.keyboard.ckb import CKB
from Services.TelegramBotService.utils.keyboard.ikb import IKB
from Infrastructure.Posthog.Posthog import posthog_manager  # type: ignore
from Services.TelegramBotService.BotMiddlewares.UserMW import TelegramUser
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction

router = Router()


@router.message(Command("get_file_id"), ManagerFilter())  # todo get file id
async def get_file_id_tool(message: Message, state: FSMContext) -> None:
    await state.set_state(state=ToolState.tool)


@router.message(ToolState.tool)
async def get_file_id_tool_state(message: Message) -> None:
    if message.voice:
        await message.answer(text=message.voice.file_id)
    elif message.document:
        await message.answer(message.document.file_id)
    elif message.photo:
        await message.answer(message.photo[0].file_id)
    elif message.video_note:
        await message.answer(text=message.video_note.file_id)
    elif message.video:
        await message.answer(text=message.video.file_id)
    elif message.sticker:
        await message.answer(message.sticker.file_id)


@router.message(Command("send_broadcast"), ManagerFilter())  # todo malling
async def send_broadcast_tool(message: Message, state: FSMContext) -> None:
    await state.set_state(state=ToolState.start_mallin)
    await message.answer(text="Отправьте сообщение, которое надо разослать")


@router.message(ToolState.start_mallin)  # TODO служебное
async def send_broadcast_state_malling_tool(message: Message, state: FSMContext, telegram_user: TelegramUser) -> None:
    await state.update_data(message_id=message.message_id)
    await state.set_state(state=ToolState.send_broadcast)

    data: dict[str, Any] = await state.get_data()
    message_id: int | None = data.get('message_id')
    assert message_id is not None, "message_id is None"
    assert message.bot is not None, "message.bot is None"

    await message.bot.copy_message(
        from_chat_id=telegram_user.id,
        chat_id=telegram_user.id,
        message_id=message_id,
        parse_mode='HTML',
    )
    await message.answer(
        text=ToolText.mailing_confirmation,
        reply_markup=CKB()
        .row(text='yes')
        .row(text='No')
    )


@router.message(ToolState.send_broadcast)  # TODO служебное
@transaction()  # type: ignore
async def send_broadcast_state_tool(message: Message, state: FSMContext, telegram_user: TelegramUser) -> None:
    if message.text == "yes":
        await posthog_manager.lead_state(user_id=str(object=telegram_user.id), state="mailing_admin", data=telegram_user.model_dump())
        await message.answer(ToolText.mailing_confirmated)
        data: dict[str, Any] = await state.get_data()
        message_id: int | None = data.get('message_id')
        users: Sequence[User] = await User.select().all()

        async def send_message(message: Message, chat_id: str) -> None:
            with suppress(Exception):
                assert message_id is not None, "message_id is None"
                assert message.bot is not None, "message.bot is None"

                message_data: MessageId = await message.bot.copy_message(
                    from_chat_id=telegram_user.id,
                    chat_id=chat_id,
                    message_id=message_id,
                    parse_mode='HTML',
                )

                await posthog_manager.lead_state(user_id=chat_id, state="send_broadcast", data=message_data.model_dump())

        async with anyio.create_task_group() as tg:
            for user in users:
                tg.start_soon(send_message, message, str(user.id))

        await message.answer(text=ToolText.mailing_end)
    else:
        await message.answer(text=ToolText.mailing_canceled)

    await state.clear()


@router.message(Command("wa"))
async def webapp(message: Message, command: CommandObject) -> None:
    assert command.args
    await message.answer(
        text='TestWaLink',
        reply_markup=IKB()
        .row(text='TestWaLinkKB', web_app=WebAppInfo(url=command.args))
    )

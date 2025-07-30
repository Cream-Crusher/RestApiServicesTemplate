from typing import Any

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo

from Infrastructure.PostHog.PosthogManager import posthog_manager  # type: ignore
from Services.TelegramBotService.BotMiddlewares.UserMW import TelegramUser
from Services.TelegramBotService.handlers.manager.filters.tools_filters import (
    ManagerFilter,
)
from Services.TelegramBotService.handlers.manager.states.tool_state import ToolState
from Services.TelegramBotService.handlers.manager.texts.tool_text import ToolText
from Services.TelegramBotService.utils.keyboard.ckb import CKB
from Services.TelegramBotService.utils.keyboard.ikb import IKB
from Services.TelegramBotService.utils.message.send_copy_message import (
    send_copy_message,
)
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import transaction

router = Router()


@router.message(Command("get_file_id"), ManagerFilter())
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


@router.message(Command("send_broadcast"), ManagerFilter())
async def send_broadcast_tool(message: Message, state: FSMContext) -> None:
    await state.set_state(state=ToolState.start_mallin)
    await message.answer(text="Отправьте сообщение, которое надо разослать")


@router.message(ToolState.start_mallin)
async def send_broadcast_state_malling_tool(message: Message, state: FSMContext, telegram_user: TelegramUser) -> None:
    await state.update_data(message_id=message.message_id)
    await state.set_state(state=ToolState.send_broadcast)

    data: dict[str, Any] = await state.get_data()
    message_id: int | None = data.get("message_id")
    assert message_id is not None, "message_id is None"
    assert message.bot is not None, "message.bot is None"

    await message.bot.copy_message(
        from_chat_id=telegram_user.id,
        chat_id=telegram_user.id,
        message_id=message_id,
        parse_mode="HTML",
    )
    await message.answer(
        text=ToolText.mailing_confirmation,
        reply_markup=CKB().row(text="yes").row(text="No"),
    )


@router.message(ToolState.send_broadcast)
@transaction()  # type: ignore
async def send_broadcast_state_tool(message: Message, state: FSMContext, telegram_user: TelegramUser) -> None:
    if message.text == "yes":
        await posthog_manager.lead_state(
            user_id=str(telegram_user.id),
            state="mailing_admin",
            data=telegram_user.model_dump(),
        )
        await message.answer(ToolText.mailing_confirmated)
        data: dict[str, Any] = await state.get_data()
        message_id: int | None = data.get("message_id")
        assert message_id is not None, "message_id is None"

        for user in await User.select().order_by(User.created_at.asc()).all():
            await send_copy_message(
                user_id=user.id,
                msg_id=message_id,
                msg_chat=int(telegram_user.id),
                parse_mode="html",
            )

        await message.answer(text=ToolText.mailing_end)
    else:
        await message.answer(text=ToolText.mailing_canceled)

    await state.clear()


@router.message(Command("wa"))
async def webapp(message: Message, command: CommandObject) -> None:
    assert command.args
    await message.answer(
        text="TestWaLink",
        reply_markup=IKB().row(text="TestWaLinkKB", web_app=WebAppInfo(url=command.args)),
    )


@router.message(Command("broadcast_user_id"))
async def broadcast_chat_botton_on(msg: Message, telegram_user: TelegramUser, command: CommandObject):
    if str(telegram_user.id) not in ["1001631806"]:
        return

    assert msg.reply_to_message and command.args

    for user_id in command.args.splitlines():
        await send_copy_message(
            int(user_id.strip()),
            msg_chat=msg.chat.id,
            msg_id=msg.reply_to_message.message_id,
            parse_mode="markdown",
        )
    await msg.answer("ok")

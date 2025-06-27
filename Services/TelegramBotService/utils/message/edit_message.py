from aiogram.types.message import Message
import anyio
from aiogram.exceptions import TelegramRetryAfter
from typing import Any

from Infrastructure.Posthog.Posthog import posthog_manager
from Services.TelegramBotService.get_bot import get_bot

lim = anyio.CapacityLimiter(2)


async def edit_message(user_id: int, message_id: int, text: str, **kw: Any) -> None | bool:
    async with lim:
        for i in range(4):
            try:
                msg: Message | bool = await get_bot().edit_message_text(
                    text,
                    chat_id=user_id,
                    message_id=message_id,
                    **kw,
                )
                await posthog_manager.lead_state(
                    user_id=str(user_id),
                    state="broadcast_edit",
                    data={"message_id": msg.message_id},  # type: ignore
                )
                return
            except TelegramRetryAfter as e:
                if (
                    i == 3
                    or "message is not modified" in str(e)
                    or "blocked" in str(e)
                    or "chat not found" in str(e)
                ):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_edit_fail",
                        data={"error": str(e)},
                    )

                    return
                else:
                    await anyio.sleep(min(i**3, 30))
                await anyio.sleep(e.retry_after * 2)
            except Exception as e:
                if (
                    i == 3
                    or "blocked" in str(e)
                    or "chat not found" in str(e)
                    or "message is not modified" in str(e)
                ):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_edit_fail",
                        data={"error": str(e)},
                    )
                    return
                else:
                    await anyio.sleep(min(i**3, 30))
        await anyio.sleep(0.4)
    return False

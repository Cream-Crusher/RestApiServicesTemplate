from typing import Any

import anyio
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import MessageId

from Infrastructure.Posthog.Posthog import posthog_manager
from Services.TelegramBotService.get_bot import get_bot

lim = anyio.CapacityLimiter(2)


async def send_copy_message(user_id: int, msg_id: int, msg_chat: int, **kw: Any) -> None | bool:
    async with lim:
        for i in range(4):
            try:
                msg: MessageId = await get_bot().copy_message(
                    user_id,
                    message_id=msg_id,
                    from_chat_id=msg_chat,
                    **kw,
                )
                await posthog_manager.lead_state(
                    user_id=str(user_id),
                    state="send_broadcast",
                    data={"message_id": msg.message_id},
                )

                return
            except TelegramRetryAfter as e:
                if i == 3 or "blocked" in str(e) or "chat not found" in str(e):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_fail",
                        data={"error": str(e)},
                    )
                    return
                else:
                    await anyio.sleep(min(i**3, 30))
                await anyio.sleep(e.retry_after * 2)
            except Exception as e:
                if i == 3 or "blocked" in str(e) or "chat not found" in str(e):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_fail",
                        data={"error": str(e)},
                    )
                    return
                else:
                    await anyio.sleep(min(i**3, 30))
        await anyio.sleep(0.4)
    return False

from typing import Any

import anyio
from aiogram.exceptions import TelegramRetryAfter

from Infrastructure.PostHog.PosthogManager import posthog_manager
from Services.TelegramBotService.get_bot import get_bot

lim = anyio.CapacityLimiter(2)


async def delete_message(user_id: int, message_id: int, **kw: Any) -> None | bool:
    async with lim:
        for i in range(4):
            try:
                msg: bool = await get_bot().delete_message(
                    chat_id=user_id,
                    message_id=message_id,
                    **kw,
                )
                await posthog_manager.lead_state(
                    user_id=str(user_id),
                    state="broadcast_delete",
                    data={"success": msg},  # type: ignore
                )
                return None
            except TelegramRetryAfter as e:
                if i == 3 or "message is not modified" in str(e) or "blocked" in str(e) or "chat not found" in str(e):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_delete_fail",
                        data={"error": str(e)},
                    )

                    return None
                else:
                    await anyio.sleep(min(i**3, 30))
                await anyio.sleep(e.retry_after * 2)
            except Exception as e:
                if i == 3 or "blocked" in str(e) or "chat not found" in str(e) or "message is not modified" in str(e):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_delete_fail",
                        data={"error": str(e)},
                    )
                    return None
                else:
                    await anyio.sleep(min(i**3, 30))
        await anyio.sleep(0.4)
    return False

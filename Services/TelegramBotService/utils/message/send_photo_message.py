from typing import Any

import anyio
from aiogram.exceptions import TelegramRetryAfter

from Infrastructure.PostHog.PosthogManager import posthog_manager
from Services.TelegramBotService.get_bot import get_bot

lim = anyio.CapacityLimiter(2)


async def send_photo(user_id: int, text: str, photo_url: str, disable_notification: bool = False, **kw: Any) -> None | bool:
    async with lim:
        for i in range(4):
            try:
                msg = await get_bot().send_photo(
                    user_id,
                    photo=photo_url,
                    caption=text,
                    disable_notification=disable_notification,
                    **kw,
                )
                await posthog_manager.lead_state(
                    user_id=str(user_id),
                    state="broadcast_sent",
                    data={"message_id": msg.message_id, "text": text},
                )
                return None
            except TelegramRetryAfter as e:
                if i == 3 or "blocked" in str(e) or "chat not found" in str(e):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_sent_fail",
                        data={"error": str(e)},
                    )
                    return None
                else:
                    await anyio.sleep(min(i**3, 30))
                await anyio.sleep(e.retry_after * 2)
            except Exception as e:
                if i == 3 or "blocked" in str(e) or "chat not found" in str(e):
                    await posthog_manager.lead_state(
                        user_id=str(user_id),
                        state="broadcast_sent_fail",
                        data={"error": str(e)},
                    )
                    return None
                else:
                    await anyio.sleep(min(i**3, 30))
        await anyio.sleep(0.4)
    return False

from typing import Any

from aiogram.types import Chat
from posthog import Posthog

from config import settings


class PosthogManager:

    def __init__(self, token: str | None = None) -> None:
        self.posthog = Posthog(api_key=token, host='https://hog.trendsurfers.ru')

    async def lead_start(self, user_id: str, referral: str | None, user: Chat) -> None:
        user_data: dict[str, Any] = user.model_dump()
        self.posthog.identify(  # type: ignore
            distinct_id=user_id,
            properties={
                "referral": referral,
                **user_data,
                "$set": {**user_data, "referral": referral},
            }
        )

    async def lead_state(self, user_id: str, state: str, data: dict[str, Any] | None = None) -> None:
        self.posthog.capture(  # type: ignore
            distinct_id=user_id,
            event=state,
            properties=data
        )


posthog_manager: PosthogManager = PosthogManager(
    token=settings.posthog_config.token
)

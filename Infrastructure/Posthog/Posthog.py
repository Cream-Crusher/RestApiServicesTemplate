from typing import Dict, Any

from aiogram.types import Chat
from posthog import Posthog

from Services.TemplateApiServise.WebApi.config import settings


class PosthogManager:

    def __init__(self, token: str):
        self.posthog = Posthog(token, 'https://hog.trendsurfers.ru')

    async def lead_start(self, user_id: str, referral: str | None, user: Chat) -> None:
        user_data = user.model_dump()
        self.posthog.identify(
            user_id,
            {
                "referral": referral,
                **user_data,
                "$set": {**user_data, "referral": referral},
            }
        )

    async def lead_state(self, user_id: str, state: str, data: Dict[str, Any] | None = None) -> None:
        self.posthog.capture(
            user_id,
            state,
            data
        )


PosthogMan: PosthogManager = PosthogManager(
    token=settings.posthog_config.token
)

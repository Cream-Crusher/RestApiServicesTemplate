from typing import Any

from loguru import logger
from posthog import Posthog

from config import settings


class PosthogManager:

    def __init__(self, token: str | None = None) -> None:
        logger.info(f"PosthogManager init token: {token}")
        self.posthog = Posthog(api_key=token if token else 'None', host='')

    async def lead_register(self, user_id: str, referral: str = 'self', user_data: dict[str, Any] = {}) -> None:
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

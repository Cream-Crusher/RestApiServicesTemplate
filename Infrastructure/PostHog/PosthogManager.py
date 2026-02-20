from typing import Any

from loguru import logger
from posthog import Posthog

from config import config


class PosthogManager:

    def __init__(self, host: str, token: str | None = None) -> None:
        logger.info(f"PosthogManager init token: {token}")
        self.posthog = Posthog(token if token else "None", host=host)

    async def lead_register(
        self, user_id: str, referral: str = "self", user_data: dict[str, Any] | None = None
    ) -> None:
        if user_data is None:
            user_data = {}

        self.posthog.identify(  # type: ignore
            distinct_id=user_id,
            properties={
                "referral": referral if referral else "self",
                **user_data,
            },
        )

    async def lead_state(self, user_id: str, state: str, data: dict[str, Any] | None = None) -> None:
        self.posthog.capture(distinct_id=user_id, event=state, properties=data)  # type: ignore


posthog_manager: PosthogManager = PosthogManager(token=config.posthog_config.token, host=config.posthog_config.host)

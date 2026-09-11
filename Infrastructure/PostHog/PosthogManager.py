from typing import Any

from loguru import logger
from posthog import Posthog

from config import config


class PosthogManager:

    def __init__(self, host: str, token: str | None = None) -> None:
        self.posthog: Posthog | None = None

        if not token:
            logger.warning("PostHog is disabled: empty token")
            return

        self.posthog = Posthog(token, host=host)

    async def lead_register(
        self, user_id: str, referral: str = "self", user_data: dict[str, Any] | None = None
    ) -> None:
        if self.posthog is None:
            return

        if user_data is None:
            user_data = {}

        self.posthog.set(
            distinct_id=user_id,
            properties={
                "referral": referral if referral else "self",
                "environment": config.app_config.environment,
                **user_data,
            },
        )

    async def lead_state(self, user_id: str, state: str, data: dict[str, Any] | None = None) -> None:
        if self.posthog is None:
            return

        if data is None:
            data = {}

        self.posthog.capture(
            event=state, distinct_id=user_id, properties={"environment": config.app_config.environment, **data}
        )


posthog_manager: PosthogManager = PosthogManager(token=config.posthog_config.token, host=config.posthog_config.host)

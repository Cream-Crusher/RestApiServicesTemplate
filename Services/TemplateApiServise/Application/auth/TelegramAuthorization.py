from typing import Annotated

from aiogram.utils.web_app import (
    WebAppInitData,
    WebAppUser,
    safe_parse_webapp_init_data,
)
from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader

from config import EnvironmentEnum, config
from Services.TemplateApiServise.Application.common.utcnow import utcnow

is_local = config.app_config.environment == EnvironmentEnum.LOCAL


def init_data_dependency(
    auth: Annotated[str, Depends(dependency=APIKeyHeader(name="Authorization"))],
) -> WebAppInitData:
    try:
        if is_local:
            return WebAppInitData(
                user=WebAppUser(id=int(auth), first_name="cream"),
                auth_date=utcnow(),
                hash="",
            )

        return safe_parse_webapp_init_data(token=config.bot_config.token, init_data=auth)
    except ValueError:
        raise HTTPException(403, detail="Invalid init data signature")


def get_me_telegram(
    auth_data: Annotated[WebAppInitData, Depends(init_data_dependency)],
) -> WebAppUser:

    if auth_data.user is None:
        raise HTTPException(403, detail="Forbidden")

    return auth_data.user

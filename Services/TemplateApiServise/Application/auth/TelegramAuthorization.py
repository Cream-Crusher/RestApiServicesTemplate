from typing import Annotated

from aiogram.utils.web_app import (
    WebAppInitData,
    WebAppUser,
    safe_parse_webapp_init_data,
)
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader

from config import EnvironmentEnum, config
from Services.TemplateApiServise.Application.common.exceptions.BaseApiError import BaseApiError
from Services.TemplateApiServise.Application.common.utils.utcnow import utcnow

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
        raise BaseApiError(
            status_code=403,
            error="INVALID_INITDATA",
            message="Invalid init data signature",
            detail={"init_data": auth},
        )


def get_me_telegram(
    auth_data: Annotated[WebAppInitData, Depends(init_data_dependency)],
) -> WebAppUser:

    if auth_data.user is None:
        raise BaseApiError(status_code=403, error="FORBIDDEN", message="auth_data.user is None")

    return auth_data.user

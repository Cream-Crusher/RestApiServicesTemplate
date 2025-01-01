from typing import Annotated
from urllib.parse import unquote
from aiogram.utils.web_app import WebAppInitData
from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader

from Shared.Base.config import settings


async def init_data_dependency(
        auth: Annotated[str, Depends(APIKeyHeader(name="Authorization"))],
):
    init_data = unquote(auth)

    return safe_parse_webapp_init_data(settings.bot_config.token, init_data)


async def get_me(init_data: Annotated[WebAppInitData, Depends(init_data_dependency)]):
    user = init_data.user

    return user

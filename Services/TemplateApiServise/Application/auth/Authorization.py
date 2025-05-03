from datetime import datetime
from typing import Annotated
from urllib.parse import unquote

from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppUser, WebAppInitData
from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader

from config import settings

is_local = settings.app_config.environment_type == 'local'


async def init_data_dependency(
        auth: Annotated[str, Depends(dependency=APIKeyHeader(name="Authorization"))],
) -> WebAppInitData:
    try:
        if is_local:
            return WebAppInitData(
                user=WebAppUser(
                    id=int(auth),
                    first_name='cream'
                ),
                auth_date=datetime(2025, 5, 10),
                hash=''
            )

        init_data: str = unquote(auth)
        return safe_parse_webapp_init_data(token=settings.bot_config.token, init_data=init_data)
    except ValueError:
        raise HTTPException(403, detail="Invalid init data signature")


async def get_me(
        auth_data: Annotated[WebAppInitData, Depends(init_data_dependency)]
) -> WebAppUser:

    if auth_data.user is None:
        raise HTTPException(500, detail="Unknown error")

    return auth_data.user

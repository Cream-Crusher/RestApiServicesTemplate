from typing import Annotated, Optional, Union
from urllib.parse import unquote

from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppUser, WebAppInitData
from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

from config import settings


class WebAppUserDev(BaseModel):
    id: int
    is_bot: Optional[bool] = None
    first_name: str = 'cream'
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None


async def init_data_dependency(
        auth: Annotated[str, Depends(dependency=APIKeyHeader(name="Authorization"))],
) -> WebAppInitData:
    try:
        init_data: str = unquote(auth)
        return safe_parse_webapp_init_data(token=settings.bot_config.token, init_data=init_data)
    except ValueError:
        raise HTTPException(403, detail="Invalid init data signature")


async def get_me(
        auth_data: Annotated[WebAppInitData, Depends(init_data_dependency)]
) -> Union[WebAppUser, WebAppUserDev]:

    if auth_data.user is None:
        raise HTTPException(500, detail="Unknown error")

    return auth_data.user


# dev
# async def get_me(
#         auth_data: Annotated[int, Depends(APIKeyHeader(name="Authorization"))]
# ) -> Union[WebAppUser, WebAppUserDev]:
#     return WebAppUserDev(id=auth_data)

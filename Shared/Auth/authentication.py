from typing import Annotated, Optional, Type
from urllib.parse import unquote
from aiogram.utils.web_app import WebAppInitData, WebAppUser
from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

from Shared.Base.config import settings


class WebAppUserTest(BaseModel):
    id: int = 1001631806
    is_bot: Optional[bool] = None
    first_name: str = 'first_name_test'
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None


async def init_data_dependency(
        auth: Annotated[str, Depends(APIKeyHeader(name="Authorization"))],
):
    init_data = unquote(auth)

    return safe_parse_webapp_init_data(settings.bot_config.token, init_data)


async def get_me(init_data: Annotated[WebAppInitData, Depends(init_data_dependency)]) -> WebAppUser:
    user = init_data.user
    assert user is not None, 'WebAppInitData is Null'

    return user


async def get_me_test() -> Type[WebAppUserTest]:
    return WebAppUserTest
